# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from authentication.models import User
# # Register your models here.
# class UserModelAdmin(BaseUserAdmin):
#     list_display = ('email', 'firstname', 'lastname', 'is_admin','user_type_choices')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         ('User Credentials', {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('firstname', 'lastname')}),
#         ('Permissions', {'fields': ('is_admin','user_type_choices')}),
#     )

#     search_fields = ('email', 'firstname',)
#     filter_horizontal = ()

# admin.site.register(User,UserModelAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from .models import User

class UserModelAdmin(BaseUserAdmin):
    list_display = ('email', 'firstname', 'lastname', 'is_admin', 'user_type_choice')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname')}),
        ('Permissions', {'fields': ('is_admin', 'user_type_choice')}),
    )

    search_fields = ('email', 'firstname',)
    filter_horizontal = ()
    ordering = ('email',)  # Use 'email' field for ordering

admin.site.register(User, UserModelAdmin)
admin.site.register(Permission)
