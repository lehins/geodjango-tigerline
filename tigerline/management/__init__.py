import os, sys, datetime, json
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

try:
    from django.contrib.gis.utils import LayerMapping
except ImportError:
    print("gdal is required")
    sys.exit(1)

from tigerline.utils import get_tigerline_model, get_tigerline_model_name

class BaseImportCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--path', default='', dest='path',
                    help='The directory where the data is stored.'),
        make_option('--mapping', default='', dest='mapping',
                    help='JSON file with mapping data.')
    )
    setting_name = None
    default_mapping = None

    @property
    def model_name(self):
        return get_tigerline_model_name(self.setting_name)

    @property
    def model(self):
        return get_tigerline_model(self.setting_name)
    
    @property
    def help(self):
        return 'Installs the tigerline files for %s' % self.setting_name


    def import_data(self, shp, mapping=None):
        mapping = mapping or self.default_mapping
        lm = LayerMapping(get_tigerline_model(self.setting_name),
                          shp, mapping, encoding='LATIN1')
        lm.save(verbose=True, progress=True, strict=True)

    def handle_import(self, path, mapping):
        raise NotImplementedError(
            "Cannot handle data import from the base class.")


    def handle(self, *args, **kwargs):
        path = kwargs['path']
        mapping_path = kwargs['mapping']
        mapping = None
        if mapping_path:
            if os.path.exists(mapping_path):
                file = open(mapping_path)
                mapping = json.loads(file.read())
            else:
                print('Could not find mapping json file: %s.' % mapping_path)
                sys.exit(1)
        # With DEBUG=True this will DIE.
        settings.DEBUG = False
        print("Start %s: %s" % (self.model_name, datetime.datetime.now()))
        self.handle_import(path, mapping)
        print("End %s: %s" % (self.model_name, datetime.datetime.now()))
