import os, sys

from tigerline.management import BaseImportCommand


class Command(BaseImportCommand):
    setting_name = 'TIGERLINE_COUNTY_MODEL'

    default_mapping = {
        "id": "GEOID",
        "state": {
            "fips_code": "STATEFP"
        },
        "state_fips_code": "STATEFP",
        "fips_code": "COUNTYFP",
        "name": "NAME",
        "legal_statistical_description": "LSAD",
        "mpoly": "POLYGON"
    }

    def handle_import(self, path, mapping):
        names = (
            ('2015', 'tl_2015_us_county.shp'),
            ('2014', 'tl_2014_us_county.shp'),
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
                break
        else:
            print('Could not find files.')
            sys.exit(1)
        print('Found %s County files.' % year)
        self.import_data(path, mapping)
