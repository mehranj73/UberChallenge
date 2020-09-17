import pytest
from channels.testing import WebsocketCommunicator
from routing import application
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

#Testing :

    # 1 ) can_connect_to_server : DONE
    # 2 ) can_send_message_to_server : DONE
    # 3 ) can_receive_message_from_server :  DONE
    # 4 ) can_broadcast_message_to_server : TODO
    # 5 ) can_receive_broadcasted_message_from_server : TODO

@pytest.mark.asyncio
class TestWebsocket:
    async def test_can_connect_to_server(self, settings):
        print(settings)
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application, "/trips/")
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_can_send_message_to_server(self, settings):
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application, "/trips/")
        connected, _ = await communicator.connect()
        #sending message
        message = {"type": "echo.message", "data": "this is a basic message"}
        await communicator.send_json_to(message)
        #receiving message
        response = await communicator.receive_json_from()
        assert response["data"] == message["data"]

        await communicator.disconnect()

    async def test_can_broadcast_message_to_group(self, settings):
        settings.CHANNEL_LAYERS = CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path=f"/trips/"
        )
        connected, _ = await communicator.connect()
        channel_layer = get_channel_layer()
        message = {
            "type" : "echo.message",
            "text" : "Message broadcasted to test only"
        }
        #send message to all channels in test group
        await channel_layer.group_send("test",message)
        #retrieve message
        response = await communicator.receive_json_from()
        assert response.data == message
        await communicator.disconnect()
