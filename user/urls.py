#emall\user\urls.py

from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)




urlpatterns = [
    path('',  index, name="index"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password')
]
