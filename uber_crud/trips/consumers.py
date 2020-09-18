from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async #Db interraction inside async code
from django.contrib.auth.models import AnonymousUser




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


class TripConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self): # changed
        print("Running connection \n")
        #TODO : REMOVE TEST GROUP
        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )
        print("Authentication .... \n")
        access = self.scope["query_string"].decode("utf-8")
        self.user = await get_user(access=access)
        self.user_group = await database_sync_to_async(self.user.groups.first)()
        print(f"given user : {self.user}\n")
        if self.user_group and self.user_group.name == "driver":
            await self.channel_layer.group_add(
                group='driver',
                channel=self.channel_name
            )
            print("User joined the driver group")
        await self.accept()

    async def echo_message(self, message):
        print(f"sending : {message}")
        await self.send_json({
            "type" : message["type"],
            "data" : message["data"]
        })

    async def receive_json(self, content):
        #Extracting the type
        type = content["type"]
        print(f"reecived type : {type} \n")
        if type == "echo.message":
            await self.echo_message(content)

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

        await super().disconnect(code)
