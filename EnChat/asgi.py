import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EnChat.settings")
django.setup()  # Ensures Django is fully loaded before importing anything else


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from chat.middleware import TokenAuthMiddleware
from channels.auth import AuthMiddlewareStack


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
