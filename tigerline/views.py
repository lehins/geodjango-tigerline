from django.contrib.gis.db.models.fields import GeometryField
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.core import serializers
from django.utils import simplejson as json
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.decorators.gzip import gzip_page
from django.utils.decorators import method_decorator

from tigerline.models import *
import simplekml
from sendfile import sendfile

models = {
    'division': Division,
    'state': State,
    'county': County,
    'subcounty': SubCounty
}

@login_required
def geojson_view(request, level):
    try:
        model = models[level]
    except KeyError:
        raise Http404
    params = dict([(key, request.GET[key].split(',')) for key in request.GET])
    objects = model.objects.filter(**params)
    field_names = [f.name for f in objects.model._meta.fields 
                   if not isinstance(f, GeometryField)]
    return HttpResponse(serializers.serialize(
        'geojson', objects, fields=field_names))


class KMLView(SingleObjectMixin, View):
    http_method_names = ['get']
    pk_url_kwarg = 'fips'
    format = 'kml'


    @method_decorator(gzip_page)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(KMLView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.get_object()
        profile_name = kwargs.get('profile_name', 'original')
        f = obj.get_kml(profile_name=profile_name)
        if not f:
            raise Http404
        return sendfile(request, f.path)
        
