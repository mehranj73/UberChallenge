from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from trips.consumers import TripConsumer


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
            URLRouter([
                path("trips/", TripConsumer),
            ])
        ),
})
