from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import SiteView, SiteDetailView
urlpatterns = [
    path('site/', SiteView.as_view(), name='site'),
    path('site_details/<int:pk>', SiteDetailView.as_view(), name='site_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)