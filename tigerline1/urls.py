from django.conf.urls import patterns, include, url
from tigerline.models import *
from tigerline.views import KMLView

kml_patterns = patterns('',
    url(r'^nation/(?P<pk>\w+).kml$', 
        KMLView.as_view(model=Nation), name='nation'),
    url(r'^division/(?P<pk>\d+).kml$', 
        KMLView.as_view(model=Division), name='division'),
    url(r'^state/(?P<pk>\d+).kml$', 
        KMLView.as_view(model=State), name='state'),
    url(r'^county/(\d+)/(?P<pk>\d+).kml$',  
        KMLView.as_view(model=County), name='county'),
    url(r'^subcounty/(\d+)/(\d+)/(?P<pk>\d+).kml$', 
        KMLView.as_view(model=SubCounty), name='subcounty'),
)
urlpatterns = patterns('',
    url(r'^kml/', include(kml_patterns, namespace='kml')),
)
