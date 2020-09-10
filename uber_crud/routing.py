from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import path


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
            URLRouter([
                path("trips/create/", AdminChatConsumer),
            ])
        ),
})
