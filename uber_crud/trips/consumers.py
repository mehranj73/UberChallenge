from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync

class TripConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self): # changed
        print("Running connection \n")
        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )
        print("You have been added to the test group ! \n")
        await self.accept()

    async def echo_message(self, message):
        print(f"sending : {message}")
        await self.send_json({
            "type" : message["type"],
            "data" : message["data"]
        })

    async def receive_json(self, content):
        print("receiving ! ")
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
        await super().disconnect(code)
