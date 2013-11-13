from django.contrib.gis import admin

from tigerline.models import State, County, SubCounty


#class ZipcodeAdmin(admin.OSMGeoAdmin):
#    list_display = ('code',)
#    search_fields = ('code',)


#class StateAdmin(admin.OSMGeoAdmin):
#    list_display = ('name', 'usps_code', 'fips_code')


#class CountyAdmin(admin.OSMGeoAdmin):
#    list_display = ('id', 'name', 'legal_statistical_description', 'fips_55_class_code', 'functional_status')
#    search_fields = ('name', 'state_fips_code')


#admin.site.register(Zipcode, ZipcodeAdmin)
#admin.site.register(State, StateAdmin)
#admin.site.register(County, CountyAdmin)
