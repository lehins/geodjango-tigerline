import datetime
import os
import sys
from optparse import make_option
from itertools import product

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

try:
    from django.contrib.gis.utils import LayerMapping
except ImportError:
    print("gdal is required")
    sys.exit(1)

from tigerline.models import State, County, SubCounty


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--path', default='', dest='path',
            help='The directory where the subcounty data is stored.'),
    )
    help = 'Installs the 2012 tigerline files for County Subdivisions'

    def _import(self, subcounty_shp):
        print("Start SubCounties: %s" % datetime.datetime.now())
        subcounty_mapping = {
            'id': 'GEOID',
            'state': {
                'id': 'STATEFP',
            },
            'county': {
                'id': 'COUNTYFP',
            },
            'fips_code': 'COUSUBFP',
            'name': 'NAME',
            'name_and_description': 'NAMELSAD',
            'legal_statistical_description': 'LSAD',
            'fips_55_class_code': 'CLASSFP',
            #'feature_class_code': 'MTFCC',
            'functional_status': 'FUNCSTAT',
            'mpoly': 'POLYGON',
            'aland': 'ALAND',
        }
        lm = LayerMapping(SubCounty, subcounty_shp, subcounty_mapping, 
                          encoding='LATIN1')
        lm.save(verbose=True, progress=True, strict=True)
        print("End SubCounties: %s" % datetime.datetime.now())

    def handle(self, *args, **kwargs):
        path_base = kwargs['path']
        state_fips_code = kwargs.pop('state_id', None)

        # With DEBUG on this will DIE.
        settings.DEBUG = False

        states = State.objects.order_by('fips_code')
        if state_fips_code:
            states = states.filter(fips_code=state_fips_code)
        # figure out which paths we want to use.
        states_imported = []
        for state in states:
            path_format = 'tl_2012_%s_cousub/tl_2012_%s_cousub.shp'
            path = os.path.join(path_base, path_format % (
                state.fips_code, state.fips_code))
            if os.path.exists(path):
                print ('Found files for state %s - %s .' % (
                    state.fips_code, state))
                self._import(path)
                states_imported.append(state.fips_code)
            else:
                print ('NOT found files for state %s - %s .' % (
                    state.fips_code, state))
