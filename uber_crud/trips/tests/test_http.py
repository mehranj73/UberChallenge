from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from trips.models import Trip
from django.contrib.auth.models import Group


PASSWORD = "passwOrd!"


def create_user(username, password, first_name, last_name, group="rider"):
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    user.save()
    group, _ = Group.objects.get_or_create(name=group)
    user.groups.add(group)
    print("user created ! ")
    return user

def create_trip(from_user=None, driver=None, pickup_address="Adress A", dropoff_address="Address B"):
    trip, _ = Trip.objects.get_or_create(
        from_user=from_user,
        driver=driver,
        pickup_address=pickup_address,
        dropoff_address=dropoff_address
    )
    trip.save()
    return trip



#TEST TO DO :

# 1 ) test_can_retrieve_trips_by_user
# 2 ) test_can_get_trip_by_id
# 3 ) test_can_retrieve_filtered_trips_by_user


class TripTests(APITestCase):

    def setUp(self):
        user = create_user(
            "driver@test.com",
            PASSWORD,
            "test",
            "Mr Test"
        )
        response = self.client.post(reverse("login"), {"username": user.username, "password" : PASSWORD})
        self.access = response.data["access"]

    def test_can_retrieve_trips_list(self):
        trips = [
            Trip.objects.create(pickup_address="Pickup 1", dropoff_address="Pickup 1.1"),
            Trip.objects.create(pickup_address="Pickup 2", dropoff_address="Pickup 2.1")
        ]
        actual_id = [trip.id for trip in trips]
        url = reverse("list_trip")
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer '+ self.access)
        expected_id = [trip["id"] for trip in response.data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual_id, expected_id)

    def test_can_retrieve_trip_by_id(self):
        trip = create_trip()
        trip_id = trip.id
        url = reverse("trip_detail", args=[trip_id])
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer '+ self.access)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], trip.id)
        self.assertEqual(response.data["pickup_address"], trip.pickup_address)

    def test_can_retrieve_trips_by_user(self):
        user = create_user("driver2@test.com",PASSWORD,"test","Mr Test", group="rider")
        # ####BAD CODE : SAME AS SETUP ! ! DRY
        response = self.client.post(reverse("login"), {"username": user.username, "password" : PASSWORD})
        self.access = response.data["access"]
        #####

        trips = [
            Trip.objects.create(pickup_address="Pickup 1", dropoff_address="Pickup 1.1", from_user=user, status="IN_PROGRESS"),
            Trip.objects.create(pickup_address="Pickup 2", dropoff_address="Pickup 2.1", from_user=user, status="IN_PROGRESS"),
            Trip.objects.create(pickup_address="Pickup 3", dropoff_address="Pickup 3333", from_user=user, status="COMPLETED"),
        ]
        url = reverse("list_trip") + "?status=COMPLETED" #getting all COMPLETED triped !
        print(url)
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer '+ self.access)
        print("returned ! ")
        print(response.data)
        print("here is the user !")
        print(user)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(user.id, response.data[0]["username"])
        self.assertEqual(trips[2].id, response.data[0]["id"])
        self.assertEqual(trips[2].status, response.data[0]["status"])
