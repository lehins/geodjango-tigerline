from django.contrib.gis import admin


#class ZipcodeAdmin(admin.OSMGeoAdmin):
#    list_display = ('code',)
#    search_fields = ('code',)


class NationAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

class DivisionAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

class StateAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'usps_code', 'fips_code')
    search_fields = ('name', 'fips_code')


class CountyAdmin(admin.OSMGeoAdmin):
    list_display = (
        'name', 'state', 'fips_code', 'legal_name'
    )
    list_filter = ('state',)
    search_fields = ('name', 'state__name')

class SubCountyAdmin(admin.OSMGeoAdmin):
    list_display = (
        'name', 'county', 'state', 'fips_code', 'legal_name'
    )
    readonly_fields = ('name', 'county', 'state', 'fips_code', 'legal_name')
    list_filter = ('state',)
    search_fields = ('name', 'county__name', 'state__name')


#admin.site.register(Zipcode, ZipcodeAdmin)
#admin.site.register(State, StateAdmin)
#admin.site.register(County, CountyAdmin)
