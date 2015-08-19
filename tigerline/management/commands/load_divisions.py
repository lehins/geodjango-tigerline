from django.contrib.gis.geos import Polygon, MultiPolygon
from django.contrib.gis.db.models import Union
from django.core.management.base import BaseCommand

from tigerline.codes import DIVISIONS
from tigerline.utils import get_tigerline_model


class Command(BaseCommand):
    help = "Creates divisions from states' geometry."

    def handle(self, *args, **kwargs):
        State = get_tigerline_model('TIGERLINE_STATE_MODEL')
        Division = get_tigerline_model('TIGERLINE_DIVISION_MODEL')
        for division_id, division_name in DIVISIONS:
            print "Started %s" % division_name
            states = State.objects.filter(division=division_id)
            mpoly = states.aggregate(Union('mpoly'))['mpoly__union']
            if isinstance(mpoly, Polygon):
                mpoly = MultiPolygon(mpoly)
            try:
                division = Division.objects.get(pk=division_id)
                division.mpoly = mpoly
                division.name = division_name
                division.save()
            except Division.DoesNotExist:
                Division.objects.create(
                    id=division_id, mpoly=mpoly, name=division_name)
