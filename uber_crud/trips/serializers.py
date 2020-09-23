from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields =    ["id","from_user", "driver", "pickup_address", "dropoff_address"]

    def create(self, validated_data):
        trip =  Trip.objects.create(**validated_data)
        trip.save()
        return trip

class NestedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
        depth = 1
