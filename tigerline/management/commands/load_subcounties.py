import os, sys
from distutils.util import strtobool

from tigerline.management import BaseImportCommand
from tigerline.utils import get_tigerline_model


class Command(BaseImportCommand):
    setting_name = 'TIGERLINE_SUBCOUNTY_MODEL'

    default_mapping = {
        "id": "GEOID",
        "state": {
            "fips_code": "STATEFP"
        },
        "county": {
            "state_fips_code": "STATEFP",
            "fips_code": "COUNTYFP"
        },
        "fips_code": "COUSUBFP",
        "name": "NAME",
        "legal_statistical_description": "LSAD",
        "mpoly": "POLYGON"
    }

    def handle_import(self, path, mapping):
        names = (
            ('2015', 'tl_2015_%s_cousub.shp'),
            ('2014', 'tl_2014_%s_cousub.shp'),
            ('2013', 'tl_2013_%s_cousub.shp'),
            ('2012', 'tl_2012_%s_cousub.shp'),
            ('2011', 'tl_2011_%s_cousub.shp'),
            ('2010', 'tl_2010_%s_cousub10.shp')
        )
        State = get_tigerline_model('TIGERLINE_STATE_MODEL')
        states = State.objects.filter(id__gte=25).order_by('id')
        for state in states:
            year = None
            for year, name in names:
                check_path = os.path.join(path, name % state.fips_code)
                print "Trying: %s" % check_path
                if os.path.exists(check_path):
                    print('Found %s SubCounty files for: %s.' % (year, state))
                    self.import_data(check_path, mapping)
                    break
            else:
                print('Could not find SubCounty files for: %s - %s.' % (
                    state.fips_code, state))
                incorrect = True
                while incorrect:
                    sys.stdout.write("Would you like to continue? [y/N]: ")
                    answer = raw_input() or 'no'
                    try:
                        if not strtobool(answer.lower()):
                            sys.exit(1)
                        incorrect = False
                    except ValueError:
                        print("Incorrect answer: %s" % answer)

