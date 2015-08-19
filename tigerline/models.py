from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible

from tigerline.codes import REGIONS, DIVISIONS, COUNTY_LEGAL_DESCRIPTION, \
    SUBCOUNTY_LEGAL_DESCRIPTION, LEGAL_DESCRIPTION_POSITION, COUNTY_CLASS_CODE, \
    COUNTY_FUNCTIONAL_STATUS, SUBCOUNTY_CLASS_CODES, SUBCOUNTY_FUNCTIONAL_STATUS
from tigerline.utils import get_tigerline_model_name, is_abstract

__all__ = [
    'Zipcode', 'Nation', 'Division', 'State', 'County', 'SubCounty',
    'StateComplete', 'CountyComplete', 'SubCountyComplete'
]

@python_2_unicode_compatible
class Zipcode(models.Model):
    code = models.CharField(max_length=5, unique=True)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['code']
        abstract = is_abstract('TIGERLINE_ZIPCODE_MODEL')


@python_2_unicode_compatible
class Nation(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=30)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    class Meta:
        abstract = is_abstract('TIGERLINE_NATION_MODEL')

    @property
    def legal_name(self):
        return self.name

    def __str__(self):
        return self.name

        
@python_2_unicode_compatible
class Division(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    class Meta:
        ordering = ['id']
        abstract = is_abstract('TIGERLINE_DIVISION_MODEL')

    @property
    def legal_name(self):
        return self.name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class State(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    fips_code = models.CharField(max_length=2, unique=True)
    usps_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    region = models.PositiveSmallIntegerField(choices=REGIONS)
    division = models.PositiveSmallIntegerField(choices=DIVISIONS)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    class Meta:
        ordering = ['name']
        swappable = 'TIGERLINE_STATE_MODEL'
        abstract = get_tigerline_model_name('TIGERLINE_STATE_MODEL') != 'tigerline.State'

    @property
    def legal_name(self):
        return self.name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class County(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey(
        get_tigerline_model_name('TIGERLINE_STATE_MODEL'), null=True)
    state_fips_code = models.CharField(max_length=2) 
    fips_code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    legal_statistical_description = models.PositiveSmallIntegerField(
        choices=COUNTY_LEGAL_DESCRIPTION)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = 'Counties'
        swappable = 'TIGERLINE_COUNTY_MODEL'
        abstract = get_tigerline_model_name('TIGERLINE_COUNTY_MODEL') != 'tigerline.County'

    @property
    def legal_name(self):
        name = u"%s %s" % (self.name, dict(COUNTY_LEGAL_DESCRIPTION).get(
            self.legal_statistical_description, ''))
        return name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SubCounty(models.Model):
    id = models.BigIntegerField(primary_key=True)
    state = models.ForeignKey(
        get_tigerline_model_name('TIGERLINE_STATE_MODEL'), null=True)
    county = models.ForeignKey(
        get_tigerline_model_name('TIGERLINE_COUNTY_MODEL'), null=True)
    fips_code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    legal_statistical_description = models.PositiveSmallIntegerField(
        choices=SUBCOUNTY_LEGAL_DESCRIPTION)
    mpoly = models.MultiPolygonField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = 'County Subdivision'
        swappable = 'TIGERLINE_SUBCOUNTY_MODEL'
        abstract = get_tigerline_model_name('TIGERLINE_SUBCOUNTY_MODEL') != 'tigerline.SubCounty'

    @property
    def legal_name(self):
        name = self.name
        p_or_s = dict(LEGAL_DESCRIPTION_POSITION).get(
            self.legal_statistical_description, '')
        descr = dict(SUBCOUNTY_LEGAL_DESCRIPTION).get(
            self.legal_statistical_description, '')
        if p_or_s == 'p':
            name = u"%s %s" % (descr, name)
        elif p_or_s == 's':
            name = u"%s %s" % (name, descr)
        return name

    def __str__(self):
        return self.name


# Complete set of abstract models for all objects with all available fields:        


class StateComplete(State):
    ansi_code = models.CharField(max_length=8, unique=True)
    area_description_code = models.CharField(max_length=2)
    feature_class_code = models.CharField(max_length=5)
    functional_status = models.CharField(max_length=1)
    area_land = models.BigIntegerField()
    area_water = models.BigIntegerField()
    internal_lat = models.CharField(max_length=12)
    internal_lon = models.CharField(max_length=12)

    class Meta:
        abstract = is_abstract('TIGERLINE_STATE_MODEL')
        

class CountyComplete(County):
    ansi_code = models.CharField(max_length=32)
    name_and_description = models.CharField(max_length=100)
    fips_55_class_code = models.CharField(
        max_length=2, choices=COUNTY_CLASS_CODE)
    feature_class_code = models.CharField(max_length=5)
    stat_area_code_combined = models.CharField(max_length=3)
    stat_area_code = models.CharField(max_length=5)
    division_code_metro = models.CharField(max_length=5)
    functional_status = models.CharField(
        max_length=1, choices=COUNTY_FUNCTIONAL_STATUS)
    area_land = models.BigIntegerField()
    area_water = models.BigIntegerField()
    internal_lat = models.CharField(max_length=12)
    internal_lon = models.CharField(max_length=12)

    class Meta:
        abstract = is_abstract('TIGERLINE_COUNTY_MODEL')

        
class SubCountyComplete(SubCounty):
    ansi_code = models.CharField(max_length=8)
    state_fips_code = models.CharField(max_length=2)
    county_fips_code = models.CharField(max_length=3)
    name_and_description = models.CharField(max_length=100)
    fips_55_class_code = models.CharField(
        max_length=2, choices=SUBCOUNTY_CLASS_CODES)
    feature_class_code = models.CharField(max_length=5)
    ne_combined_code = models.CharField(max_length=3)
    ne_code = models.CharField(max_length=5)
    ne_division_code = models.CharField(max_length=5)
    functional_status = models.CharField(
        max_length=1, choices=SUBCOUNTY_FUNCTIONAL_STATUS)
    area_land = models.BigIntegerField()
    area_water = models.BigIntegerField()
    internal_lat = models.CharField(max_length=12)
    internal_lon = models.CharField(max_length=12)

    class Meta:
        abstract = is_abstract('TIGERLINE_SUBCOUNTY_MODEL')
        

