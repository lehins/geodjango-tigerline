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

from tigerline.models import State, County


def county_import(county_shp):
    county_mapping = {
        'id': 'GEOID',
        'fips_code': 'COUNTYFP',
        'state_fips_code': 'STATEFP',
        'name': 'NAME',
        'name_and_description': 'NAMELSAD',
        'legal_statistical_description': 'LSAD',
        'fips_55_class_code': 'CLASSFP',
        #'feature_class_code': 'MTFCC',
        'functional_status': 'FUNCSTAT',
        'mpoly': 'POLYGON',
    }
    lm = LayerMapping(County, county_shp, county_mapping, encoding='LATIN1')
    lm.save(verbose=True, progress=True)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--path', default='', dest='path',
            help='The directory where the county data is stored.'),
    )
    help = 'Installs the 2012 tigerline files for counties'

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        # With DEBUG on this will DIE.
        settings.DEBUG = False

        # Check for existance of shape files
        if os.path.exists(os.path.join(path, 'tl_2012_us_county')):
            print('Found 2012 files.')
            path = os.path.join(path, 'tl_2012_us_county/tl_2012_us_county.shp')
        else:
            print('Could not find files.')
            exit()

        print("Start Counties: %s" % datetime.datetime.now())
        if path:
            county_import(path)
        print("End Counties: %s" % datetime.datetime.now())
        self._post_import()

    def _post_import(self, step=1000):
        states = dict([(x.fips_code, x) for x in 
                       State.objects.order_by('fips_code')])
        counties = County.objects.filter(state=None).order_by('pk')
        total = counties.count()
        for i in range(0, (total/step)+1):
            start, end = i*step, (i+1)*step-1
            cs = counties[start:end]
            for c in cs:
                c.state = states[c.state_fips_code]
                c.save()
                print "Updated: %s" % c
            print "Processed so far: %s" % (start+len(cs))
