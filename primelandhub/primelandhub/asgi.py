import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import importlib

# Set DJANGO_SETTINGS_MODULE before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'primelandhub.primelandhub.settings')

# Initialize Django ASGI application early
django_asgi_app = get_asgi_application()

# Lazy import of routing to avoid early model imports
def get_websocket_urlpatterns():
    routing = importlib.import_module('landhub.routing')
    return routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            get_websocket_urlpatterns()
        )
    ),
})
