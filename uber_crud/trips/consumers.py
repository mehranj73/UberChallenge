from channels.generic.websocket import AsyncJsonWebsocketConsumer

class TripConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        print("WELCOME ! ")
        await self.close()
