import datetime

from django.contrib.gis.geos import Polygon, MultiPolygon
from django.core.management.base import BaseCommand

from tigerline.models import *

from tigerline.models import State, Division


class Command(BaseCommand):
    help = 'Installs the 2012 tigerline files for Nation'

    def handle(self, *args, **kwargs):
        states = State.objects.all()
        mpoly = states[0].mpoly
        for state in states:
            mpoly = mpoly.union(state.mpoly)
        try:
            nation = Nation.objects.get(id='USA')
        except Nation.DoesNotExist:
            nation = Nation(id='USA', name="United Sates of America")
        nation.mpoly = mpoly.simplify(tolerance=0.001, preserve_topology=True)
        nation.kml_file = None
        nation.save()
