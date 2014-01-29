from django.contrib.gis.geos import Polygon, MultiPolygon
from django.contrib.gis.db.models import Union
from django.core.management.base import BaseCommand

from tigerline1.models import get_custom_model

class Command(BaseCommand):
    help = "Creates Nation model of United States using states' geometry."

    def handle(self, *args, **kwargs):
        State = get_custom_model('state')
        Nation = get_custom_model('nation')
        states = State.objects.all()
        mpoly = states.aggregate(Union('mpoly'))['mpoly__union']
        try:
            nation = Nation.objects.get(pk='USA')
            nation.mpoly = mpoly
            nation.name = "United Sates of America"
            nation.save()
        except Nation.DoesNotExist:
            Nation.objects.get_or_create(
                id='USA', name="United Sates of America", mpoly=mpoly)
