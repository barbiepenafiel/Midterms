from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView,
    Setup2FAView, Verify2FAView, Disable2FAView,
    UserProfileView, ChangePasswordView
)

app_name = 'authentication'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 2FA
    path('2fa/setup/', Setup2FAView.as_view(), name='2fa-setup'),
    path('2fa/verify/', Verify2FAView.as_view(), name='2fa-verify'),
    path('2fa/disable/', Disable2FAView.as_view(), name='2fa-disable'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
