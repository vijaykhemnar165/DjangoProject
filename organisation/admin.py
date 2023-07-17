from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Site
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

class SiteModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'organization', 'zipcode')


admin.site.register(Site, SiteModelAdmin)
