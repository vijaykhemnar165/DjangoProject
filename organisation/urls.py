from django.urls import path
from .views import SiteView, SiteDetailView, OrganisationView, OrganisationView
urlpatterns = [
    path('site/', SiteView.as_view(), name='site'),
    path('site_details/<int:pk>', SiteDetailView.as_view(), name='site_details'),
    path('organisation/', OrganisationView.as_view(), name='organisation'),
    path('organisation/<int:pk>', OrganisationView.as_view(), name='organisation_details'),
]