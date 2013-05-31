from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Polygon, MultiPolygon
from optparse import make_option

from tigerline.models import *
import datetime

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--model', action='store', dest='model_name', default='all',
                    type='choice', choices=['all', 'State', 'County', 'SubCounty'],
                    help='Which models to update; all=All models, state=State model,'
                    'county=County model, subcounty=SubCounty Model'),
    )
    help = 'Updates the files associated with `kml_file` field.'
    
    def _save_kml(self, obj):
        obj.smart_fields_cleanup(obj, 'kml_file')
        obj.kml_file = None
        obj.save()
        obj.kml_file.close()
        print "Saved %s - name: %s" % (obj.pk, obj.name)

    def handle(self, *args, **kwargs):
        models = {
            'State': State,
            'County': County,
            'SubCounty': SubCounty,
            }
        model_name = kwargs['model_name']
        if 'all' == model_name:
            models = [m for key, m in models.iteritems()]
        else:
            models = [models[model_name]]
        started = datetime.datetime.now()
        for model in models:
            objs = model.objects.all()
            print "Started %s" % model.__name__
            for o in objs.iterator():
                self._save_kml(o)
        if model_name in ['State', 'all']:
            print "Started Divisions."
            divisions = []
            for division_id, division_name in DIVISIONS:
                print "Started %s" % division_name
                states = State.objects.filter(division=division_id)
                mpoly = states[0].mpoly
                for state in states:
                    mpoly = mpoly.union(state.mpoly)
                try:
                    division = Division.objects.get(id=division_id)
                except Division.DoesNotExist:
                    division = Division(id=division_id, name=division_name)
                mpoly = mpoly.simplify(tolerance=0.001, preserve_topology=True)
                if isinstance(mpoly, Polygon):
                    mpoly = MultiPolygon(mpoly)
                division.mpoly = mpoly
                division.save()
                self._save_kml(division)
                divisions.append(division)
            states = State.objects.all()
            mpoly = states[0].mpoly
            for state in states:
                mpoly = mpoly.union(state.mpoly)
            try:
                nation = Nation.objects.get(id='USA')
            except Nation.DoesNotExist:
                nation = Nation(id='USA', name="United Sates of America")
            nation.mpoly = mpoly.simplify(tolerance=0.001, preserve_topology=True)
            nation.save()
            self._save_kml(nation)
        elapsed = (datetime.datetime.now()-started).total_seconds()
        print "Finished within %s minutes" % (elapsed/60)
