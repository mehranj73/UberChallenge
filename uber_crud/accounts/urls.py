from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CreateUserView,
    LoginView
)

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name="signup"),
    path('api/token/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
