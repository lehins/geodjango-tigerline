import datetime

from django.contrib.gis.geos import Polygon, MultiPolygon
from django.core.management.base import BaseCommand

from tigerline.models import *

from tigerline.models import State, Division


class Command(BaseCommand):
    help = 'Installs the 2012 tigerline files for divisions'

    def handle(self, *args, **kwargs):
        # TODO: make the tolerance as an option to set
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
            division.kml_file = None
            division.save()
