import os, sys

from tigerline1.management import BaseImportCommand


class Command(BaseImportCommand):
    object_name = 'county'

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
        print('Found %s %s files.' % (year, self.object_name.title()))
        self.import_data(path, mapping)