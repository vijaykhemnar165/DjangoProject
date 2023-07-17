from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, UserLoginView, PermissionGrantViewSet
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('permissions/', PermissionGrantViewSet.as_view({'get': 'list'}), name='permissions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)