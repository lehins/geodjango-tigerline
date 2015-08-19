from django.contrib.gis.db.models import Union
from django.core.management.base import BaseCommand

from tigerline.utils import get_tigerline_model

class Command(BaseCommand):
    help = "Creates Nation model of United States using states' geometry."

    def handle(self, *args, **kwargs):
        State = get_tigerline_model('TIGERLINE_STATE_MODEL')
        Nation = get_tigerline_model('TIGERLINE_NATION_MODEL')
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
