from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async #Db interraction inside async code
from django.contrib.auth.models import AnonymousUser
from .models import Trip
from  .serializers import TripSerializer

async def get_user(access=None):
    '''
        return a user based on token or return an anonymous user
    '''
    if not access:
        print("not access !")
        return AnonymousUser()
    try:
        access_token = AccessToken(access)
        user = await database_sync_to_async(JWTAuthentication().get_user)(access_token)
    except Exception as e:
        print("exception : ",e)
        return AnonymousUser()
    if user.is_anonymous:
        user = AnonymousUser()
    return user


async def create_trip(trip_data):
    #Serializing data
    serializer = await database_sync_to_async(TripSerializer)(data=trip_data)
    await database_sync_to_async(serializer.is_valid)(raise_exception=True)
    #user are ids here
    trip = await database_sync_to_async(serializer.create)(validated_data=serializer.validated_data)
    #return trip and serialized_trip
    print(trip.id)
    return trip

async def get_serialized_trip(trip_obj):
    serializer = await database_sync_to_async(TripSerializer)(trip_obj)
    return serializer.data

@database_sync_to_async
def get_all_trips_id(user_id, group):
    print(group)
    if group == "rider":
        trips = Trip.objects.filter(from_user=user_id)
    elif group == "driver":
        trips = Trip.objects.filter(driver=user_id)
    return [trip.id for trip in trips]


class TripConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        #TODO : REMOVE TEST GROUP
        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )
        access = self.scope["query_string"].decode("utf-8")
        self.user = await get_user(access=access)
        self.user_group = await database_sync_to_async(self.user.groups.first)()
        #TODO : GET ALL RELATED TRIPS FOR A USER
        if self.user_group:
            self.all_user_trips_id = await get_all_trips_id(self.user.id, self.user_group.name)
            if self.all_user_trips_id:
                for trip_id in self.all_user_trips_id:
                    await self.channel_layer.group_add(f"trip_{trip_id}", self.channel_name)
        if self.user_group and self.user_group.name == "driver":
            print(f"{self.user.username} is joining driver")
            await self.channel_layer.group_add(
                group='driver',
                channel=self.channel_name
            )
        elif self.user_group and self.user_group.name == "rider":
            print(f"{self.user.username} is joining rider")
            await self.channel_layer.group_add(
                group="rider",
                channel=self.channel_name
            )
        await self.accept()

    async def echo_message(self, message):
        await self.send_json({
            "type" : message["type"],
            "data" : message["data"]
        })

    async def _accept_trip(self, message):
        print(message)
        trip_id, driver_id = message["data"]["trip_id"],message["data"]["driver"]
        trip = await database_sync_to_async(Trip.objects.get)(id=trip_id)
        #TODO : WRITE FUNCTION TO UPDATE !
        serializer = await database_sync_to_async(TripSerializer)(trip, data={
            "driver" : driver_id,
            "status" : "ACCEPTED"
        }, partial=True)
        await database_sync_to_async(serializer.is_valid)(raise_exception=True)
        updated_trip = await database_sync_to_async(serializer.save)()
        #END TODO
        serialized_updated_trip = await get_serialized_trip(updated_trip)
        print("SERIALIZED UPDATED TRIP ! ")
        print(serialized_updated_trip)
        await self.channel_layer.group_add(f"trip_{trip.id}", self.channel_name)
        print("Successfully accepted the trip")
        await self.echo_message({
            "type" : "echo.message",
            "data" : serialized_updated_trip
        })


    async def _trip_success(self, message):
        print("Successfull trip creation ! ")
        await self.echo_message(message)

    async def _trip_fail(self, message):
        print("Failed to create trip :/ !")
        await self.echo_message(message)

    #TODO : FIX TRY EXCEPT BLOCK => UNWANTED MESSAGE SENT
    async def _create_trip(self, message):
        try :
            message["data"]["status"] = "REQUESTED"
            trip = await create_trip(message["data"])
            serialized_trip = await get_serialized_trip(trip)

            await self._trip_success({
                "type" : "trip.success",
                "data" : serialized_trip
            })
            #Adding current channel to the trip group : (rider side)
            await self.channel_layer.group_add(f"trip_{trip.id}", self.channel_name)
            await self.channel_layer.group_send("driver", {
                "type" : "echo.message",
                "data" : serialized_trip
            })

        except Exception as e:
            print(e)
            await self._trip_fail({
                "type" : "trip.fail",
                "data" : "Something went wrong "
            })

    async def receive_json(self, content):
        type = content["type"]
        print(f"reecived type : {type} \n")
        if type == "echo.message":
            await self.echo_message(content)
        elif type == "create.trip":
            await self._create_trip(content)
        elif type == "accept.trip":
            await self._accept_trip(content)

    #If you want to customise the JSON encoding and decoding, you can override the encode_json and decode_json classmethods.

    async def disconnect(self, code): # changed
        await self.channel_layer.group_discard(
            group='test',
            channel=self.channel_name
        )
        print("removing your connection to the test group ! \n")
        if self.user_group and self.all_user_trips_id:
            for trip_id in self.all_user_trips_id:
                await self.channel_layer.group_discard(
                    group=f"trip_{trip_id}",
                    channel=self.channel_name
                )
                print(f"You have been removed from {trip_id}")
        if self.user_group and self.user_group.name == "driver":
            await self.channel_layer.group_discard(
                group='driver',
                channel=self.channel_name
            )
            print(f"removing your connection to the {self.user_group.name} group ! \n")
        elif self.user_group and self.user_group.name == "rider":
            await self.channel_layer.group_discard(
                group="rider",
                channel=self.channel_name
            )
            print(f"removing your connection to the {self.user_group.name} group ! \n")
        await super().disconnect(code)
