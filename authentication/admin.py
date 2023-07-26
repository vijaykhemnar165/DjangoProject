from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


class CustomUserCreationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'password', 'confirm_password', 'user_type_choice', 'is_staff', 'is_superuser']

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

class UserProfileModelAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type_choice',
                                    'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'confirm_password','user_type_choice',
                       'is_staff', 'is_superuser')}
         ),
    )
    list_display = ['id','email', 'username', 'user_type_choice', 'is_active','is_customer', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username']
    ordering = ['email']

admin.site.register(UserProfile, UserProfileModelAdmin)

