from django.contrib import admin
from django.urls import path
from .views import (ListTripView, RetrieveTripView)

urlpatterns = [
    path('<int:pk>/', RetrieveTripView.as_view(), name="trip_detail"),
    path('', ListTripView.as_view(), name="list_trip")
]
