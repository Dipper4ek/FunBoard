from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Game.routing
import authentication.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Game.routing.websocket_urlpatterns +
            authentication.routing.websocket_urlpatterns
        )
    ),
})
