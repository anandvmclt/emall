#emall\user\urls.py

from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from django_rest_passwordreset.views import reset_password_confirm,reset_password_validate_token




urlpatterns = [
    path('',  index, name="index"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/',ChangePasswordView.as_view(), name='change-password'),
    path('password-forgot/', include('django_rest_passwordreset.urls', namespace='password_forgot')),
    path('password-forgot/confirm', reset_password_confirm, name='password_forgot_confirm'),
]
