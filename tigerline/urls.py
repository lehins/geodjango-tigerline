from django.conf.urls import patterns, include, url
from tigerline.models import *
from tigerline.views import KMLView
#from djgeojson.views import GeoJSONLayerView

kml_patterns = patterns('',
    url(r'^nation/(?P<fips>\w+)(?:_(?P<profile_name>selected))?.kml$', 
        KMLView.as_view(model=Nation), name='nation'),
    url(r'^division/(?P<fips>\d+)(?:_(?P<profile_name>selected))?.kml$', 
        KMLView.as_view(model=Division), name='division'),
    url(r'^state/(?P<fips>\d+)(?:_(?P<profile_name>selected))?.kml$', 
        KMLView.as_view(model=State), name='state'),
    url(r'^county/(\d+)/(?P<fips>\d+)(?:_(?P<profile_name>selected))?.kml$',  
        KMLView.as_view(model=County), name='county'),
    url(r'^subcounty/(\d+)/(\d+)/(?P<fips>\d+)(?:_(?P<profile_name>selected))?.kml$', 
        KMLView.as_view(model=SubCounty), name='subcounty'),
)
#json_patterns = patterns('',
#    url(r'^states.json$', 
#        GeoJSONLayerView.as_view(model=State), name='state'),
#)    
urlpatterns = patterns('',
    url(r'^kml/', include(kml_patterns, namespace='kml')),
    #url(r'^geojson/', include(json_patterns, namespace='geojson')),
)
