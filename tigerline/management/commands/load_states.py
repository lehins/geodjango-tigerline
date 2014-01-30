import os, sys

from tigerline.management import BaseImportCommand


class Command(BaseImportCommand):
    object_name = 'state'

    default_mapping = {
        "id": "GEOID",
        "fips_code": "STATEFP",
        "usps_code": "STUSPS",
        "name": "NAME",
        "region": "REGION",
        "division": "DIVISION",
        "mpoly": "POLYGON",
    }

    def handle_import(self, path, mapping):
        names = (
            ('2013', 'tl_2013_us_state.shp'),
            ('2012', 'tl_2012_us_state.shp'),
            ('2011', 'tl_2011_us_state.shp'),
            ('2010', 'tl_2010_us_state10.shp'),
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
