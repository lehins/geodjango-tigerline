import os, sys

from tigerline.models import get_custom_model
from tigerline.management import BaseLoadCommand


class Command(BaseImportCommand):
    object_name = 'county'

    default_mapping = {
        'id': 'GEOID',
        'fips_code': 'COUNTYFP',
        'state_fips_code': 'STATEFP',
        'state': {
            'id': 'STATEFP',
        },
        'name': 'NAME',
        'name_and_description': 'NAMELSAD',
        'legal_statistical_description': 'LSAD',
        'fips_55_class_code': 'CLASSFP',
        #'feature_class_code': 'MTFCC',
        'functional_status': 'FUNCSTAT',
        'mpoly': 'POLYGON',
        'aland': 'ALAND',
    }

    def handle_import(self, path, mapping):
        names = (
            ('2013', 'tl_2013_us_county.shp'),
            ('2012', 'tl_2012_us_county.shp'),
            ('2011', 'tl_2011_us_county.shp'),
            ('2010', 'tl_2010_us_county10.shp'),
        )
        year = None
        for year, name in names:
            check_path = os.path.join(path, name)
            if os.path.exists(check_path):
                path = check_path
                break;
        else:
            print('Could not find files.')
            sys.exit(1)
        print('Found %s %s files.' % (year, self.object_name))
        self.import_data(path, mapping)