from rest_framework import serializers
from .models import Trip



class CreateTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ["id", "from_user", "driver", "pickup_address", "dropoff_address"]
        read_only_fields = ["id"]

class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields =    ["id","from_user", "driver", "pickup_address", "dropoff_address"]
