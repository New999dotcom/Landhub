import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # Add this for WebSocket auth
import landhub.routing  # Make sure this exists

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'primelandhub.settings')  # Changed from your_project_name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # Added AuthMiddleware
        URLRouter(
            landhub.routing.websocket_urlpatterns
        )
    ),
})
