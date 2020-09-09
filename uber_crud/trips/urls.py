from django.contrib import admin
from django.urls import path
from .views import (CreateTripView, ListTripView, RetrieveTripView)

urlpatterns = [
    path('create/', CreateTripView.as_view(), name="create_trip"),
    path('<int:pk>/', RetrieveTripView.as_view(), name="trip_detail"),
    path('', ListTripView.as_view(), name="list_trip")
]
