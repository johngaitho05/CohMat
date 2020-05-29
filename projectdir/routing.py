from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url
from mainapp.consumers import NotificationConsumer

from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^messaging/chat/(?P<room_name>\w+)$', ChatConsumer),
                    url(r'', NotificationConsumer),
                    url(r'notifications/', NotificationConsumer),
                    url(r'messages/', NotificationConsumer),
                    url(r'groups/', NotificationConsumer),
                ]
            )
        )
    )

})