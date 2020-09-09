from django.shortcuts import render
from rest_framework import generics
from .serializers import (CreateTripSerializer, TripSerializer)
from .models import Trip
from rest_framework.permissions import IsAuthenticated



class CreateTripView(generics.CreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = CreateTripSerializer
    permission_classes = [IsAuthenticated]


class ListTripView(generics.ListAPIView):
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer

class RetrieveTripView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer
