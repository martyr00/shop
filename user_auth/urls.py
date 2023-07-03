from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserRegistrationView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
]