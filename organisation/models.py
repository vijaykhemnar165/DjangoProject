from django.db import models
from authentication.models import UserProfile



class Organisation(models.Model):
    organisation_name=models.CharField(max_length=150, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.OneToOneField(UserProfile, on_delete=models.CASCADE,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organisation_name

class Site(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='organizations')
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.zipcode




