from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('registration/', TokenObtainPairView.as_view(), name='registration'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]