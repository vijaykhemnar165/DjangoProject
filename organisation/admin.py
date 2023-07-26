from .models import Site, Organisation
from django.contrib import admin


class SiteModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'zipcode', 'state', 'created_by')

class OrganisationModelAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'address', 'created_by')

admin.site.register(Organisation, OrganisationModelAdmin)
admin.site.register(Site, SiteModelAdmin)
