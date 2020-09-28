from django.shortcuts import render
from rest_framework import generics
from .serializers import TripSerializer
from .models import Trip
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class ListTripView(generics.ListAPIView):
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer

    def get_queryset(self):
        print("lets")
        user = self.request.user
        user_group_name = user.groups.first().name #Works if one group by user
        status = self.request.query_params.get("status", "REQUESTED")
        if user_group_name == "driver":
            return Trip.objects.filter(driver=user, status=status)
        elif user_group_name == "rider":
            return Trip.objects.filter(from_user=user, status=status)

class RetrieveTripView(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer
