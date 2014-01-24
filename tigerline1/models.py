import os
from django.contrib.gis.db import models
from django.core.files.storage import FileSystemStorage

from tigerline.codes import *
from tigerline.utils import *

__all__ = ['Zipcode', 'Nation', 'Division', 'State', 'County', 'SubCounty',
           'get_custom_model']

class Zipcode(models.Model):
    code = models.CharField(max_length=5, db_index=True)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.code

    class Meta:
        ordering = ['code']
        abstract = is_abstract('zipcode')


class Nation(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=30)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    @property
    def legal_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = is_abstract('nation')

class Division(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    @property
    def legal_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']
        abstract = is_abstract('division')


class State(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    fips_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    objects = models.GeoManager()

    @property
    def legal_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        abstract = is_abstract('state')


class County(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey(get_model_path('state'), null=True)
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
    aland = models.BigIntegerField(null=True)

    objects = models.GeoManager()

    @property
    def legal_name(self):
        name = "%s %s" % (self.name, dict(COUNTY_LEGAL_DESCRIPTION).get(
            self.legal_statistical_description, ''))
        return name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Counties'
        abstract = is_abstract('county')


class SubCounty(models.Model):
    id = models.BigIntegerField(primary_key=True)
    state = models.ForeignKey(get_model_path('state'), null=True)
    county = models.ForeignKey(get_model_path('county'), null=True)
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
    aland = models.BigIntegerField(null=True)

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

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'County Subdivision'
        abstract = is_abstract('subcounty')


