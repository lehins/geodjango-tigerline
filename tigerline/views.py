from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.decorators.gzip import gzip_page

from tigerline.models import *
from sendfile import sendfile

class KMLView(SingleObjectMixin, View):
    http_method_names = ['get']

    @method_decorator(gzip_page)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(KMLView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if not self.object.kml_file:
            raise Http404(u"KML File for %s was not found." % self.object.legal_name)
        return sendfile(request, self.object.kml_file.path)
        
