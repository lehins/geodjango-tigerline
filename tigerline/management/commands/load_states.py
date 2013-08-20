import datetime
import os
import sys
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

try:
    from django.contrib.gis.utils import LayerMapping
except ImportError:
    print("gdal is required")
    sys.exit(1)

from tigerline.models import State


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--path', default='', dest='path',
            help='The directory where the state data is stored.'),
    )
    help = 'Installs the 2012 tigerline files for states'

    def _import(state_shp):
        state_mapping = {
            'id': 'GEOID',
            'fips_code': 'STATEFP',
            'region': 'REGION',
            'division': 'DIVISION',
            'usps_code': 'STUSPS',
            'name': 'NAME',
            #'area_description_code': 'LSAD',
            #'feature_class_code': 'MTFCC',
            #'functional_status': 'FUNCSTAT',
            'mpoly': 'POLYGON',
            'aland': 'ALAND',
        }
        lm = LayerMapping(State, state_shp, state_mapping, encoding='LATIN1')
        lm.save(verbose=True, progress=True, strict=True)

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        # With DEBUG on this will DIE.
        settings.DEBUG = False

        # Check for existance of shape files
        if os.path.exists(os.path.join(path, 'tl_2012_us_state')):
            print('Found 2012 files.')
            path = os.path.join(path, 'tl_2012_us_state/tl_2012_us_state.shp')
        else:
            print('Could not find files.')
            exit()

        print ("Start States: %s" % datetime.datetime.now())
        if path:
            self._import(path)
        print ("End States: %s" % datetime.datetime.now())
