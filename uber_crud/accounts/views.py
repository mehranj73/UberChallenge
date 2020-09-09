from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import (CreateUserSerializer,
                            CustomTokenObtainPairSerializer
                            )
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()
# Create your views here.


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() #DO WE NEED IT ?
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
