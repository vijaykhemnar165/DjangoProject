from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (ForgotPasswordView, ResetPasswordWithOTPView, SendInvitationView,
                    UserLoginView, UserRegistrationView, )

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('invite/', SendInvitationView.as_view(), name='invitation'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordWithOTPView.as_view(), name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)