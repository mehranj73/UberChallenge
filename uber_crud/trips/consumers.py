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
    return trip

async def get_serialized_trip(trip_obj):
    serializer = await database_sync_to_async(TripSerializer)(trip_obj)
    return serializer.data


class TripConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self): # changed
        #TODO : REMOVE TEST GROUP
        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )
        access = self.scope["query_string"].decode("utf-8")
        self.user = await get_user(access=access)
        self.user_group = await database_sync_to_async(self.user.groups.first)()
        if self.user_group and self.user_group.name == "driver":
            await self.channel_layer.group_add(
                group='driver',
                channel=self.channel_name
            )
        elif self.user_group and self.user_group.name == "rider":
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

    async def _trip_success(self, message):
        print("Successfull trip creation ! ")
        await self.echo_message(message)

    async def _trip_fail(self, message):
        print("Failed to create trip :/ !")
        await self.echo_message(message)

    #TODO : FIX TRY EXCEPT BLOCK => UNWANTED MESSAGE SENT
    async def _create_trip(self, message):
        try :
            trip = await create_trip(message["data"])
            serialized_trip = await get_serialized_trip(trip)
            await self._trip_success({
                "type" : "trip.success",
                "data" : serialized_trip
            })
            #Adding current channel to the trip group : (rider side)
            await self.channel_layer.group_add(f"{trip.id}", self.channel_name)
            await self.channel_layer.group_send("driver", {
                "type" : "echo.message",
                "data" : message["data"]
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

    #If you want to customise the JSON encoding and decoding, you can override the encode_json and decode_json classmethods.

    async def disconnect(self, code): # changed
        await self.channel_layer.group_discard(
            group='test',
            channel=self.channel_name
        )
        print("removing your connection to the test group ! \n")
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
