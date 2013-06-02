from django.contrib.gis.db import models
from django.core.files.storage import FileSystemStorage

from django.conf import settings

from tigerline.codes import *
from smart_fields.models import SmartKMLFileField, SmartFieldsBaseModel

import os, simplekml

LOCATION = getattr(settings, 'SENDFILE_ROOT', settings.MEDIA_ROOT)
BASE_URL = getattr(settings, 'SENDFILE_URL', settings.MEDIA_URL)

class Zipcode(models.Model):
    code = models.CharField(max_length=5, db_index=True)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.code

    class Meta:
        ordering = ['code']
        abstract = True


class KMLModel(SmartFieldsBaseModel):
    def upload_to(self, filename):
        return os.path.join(
            "tigerline/kml", self.__class__.__name__.lower(), 
            str(getattr(self, 'state_id', '')), str(getattr(self, 'county_id', '')),
            "%s.kml" % self.pk)

    kml_file = SmartKMLFileField(
        null=True, upload_to=upload_to, storage=FileSystemStorage(
            location=LOCATION, base_url=BASE_URL))

    def kml_processor(self, kml):
        for g in kml.geometries:
            g.name = self.legal_name
            g.snippet = simplekml.Snippet(content=str(self.pk), maxlines=1)
            g.polystyle = simplekml.PolyStyle(color="4000ac00")
            g.linestyle = simplekml.LineStyle(color="ff00ac00")
        return kml

    @property
    def smart_fields_settings(self):
        return {
            'kml_file': {
                'instance': self.kml_file,
                'geometry': lambda x: x.mpoly,
                'format': 'kml',
                'kml_processor': self.kml_processor,
            }
        }

    class Meta:
        abstract = True

class Nation(KMLModel):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=30)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    @property
    def legal_name(self):
        return self.name

    def __unicode__(self):
        return self.name

class Division(KMLModel):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    @property
    def legal_name(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']
    

class State(KMLModel):
    id = models.PositiveSmallIntegerField(primary_key=True)
    fips_code = models.CharField(max_length=2, unique=True)
    region = models.PositiveSmallIntegerField(choices=REGIONS)
    division = models.PositiveSmallIntegerField(choices=DIVISIONS)
    usps_code = models.CharField(max_length=2, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    #area_description_code = models.CharField(max_length=2)
    #feature_class_code = models.CharField(max_length=5)
    #functional_status = models.CharField(max_length=1)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    @property
    def legal_name(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class County(KMLModel):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey(State, null=True)
    fips_code = models.CharField(max_length=3)
    state_fips_code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    name_and_description = models.CharField(max_length=100)
    legal_statistical_description = models.PositiveSmallIntegerField(
        choices=COUNTY_LEGAL_DESCRIPTION)
    fips_55_class_code = models.CharField(
        max_length=2, choices=COUNTY_CLASS_CODE)
    #feature_class_code = models.CharField(max_length=5)
    functional_status = models.CharField(
        max_length=1, choices=COUNTY_FUNCTIONAL_STATUS)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    @property
    def legal_name(self):
        name = "%s %s" % (self.name, dict(COUNTY_LEGAL_DESCRIPTION).get(
            self.legal_statistical_description, ''))
        return name


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Counties'


class SubCounty(KMLModel):
    id = models.BigIntegerField(primary_key=True)
    state = models.ForeignKey(State, null=True)
    county = models.ForeignKey(County, null=True)
    state_fips_code = models.CharField(max_length=2)
    county_fips_code = models.CharField(max_length=3)
    fips_code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    name_and_description = models.CharField(max_length=100)
    legal_statistical_description = models.PositiveSmallIntegerField(
        choices=SUBCOUNTY_LEGAL_DESCRIPTION)
    fips_55_class_code = models.CharField(
        max_length=2, choices=SUBCOUNTY_CLASS_CODES)
    #feature_class_code = models.CharField(max_length=5)
    functional_status = models.CharField(
        max_length=1, choices=SUBCOUNTY_FUNCTIONAL_STATUS)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    @property
    def legal_name(self):
        name = self.name
        p_or_s = dict(LEGAL_DESCRIPTION_POSITION).get(
            self.legal_statistical_description, '')
        descr = dict(SUBCOUNTY_LEGAL_DESCRIPTION).get(
            self.legal_statistical_description, '')
        if p_or_s == 'p':
            name = "%s %s" % (descr, name)
        elif p_or_s == 's':
            name = "%s %s" % (name, descr)
        return name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'County Subdivision'


