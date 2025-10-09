"""
ASGI config for slutton_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import re
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.middleware import BaseMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slutton_backend.settings")

django_asgi_app = get_asgi_application()

# Import routing and middleware after Django setup
from comments import routing as comments_routing
from comments.middleware import JWTAuthMiddleware


class OriginValidatorMiddleware(BaseMiddleware):
    """
    Custom middleware to validate WebSocket origins
    Allows connections from Vercel deployments and production domains
    """
    ALLOWED_ORIGIN_PATTERNS = [
        r'^https://louisslutton\.com$',
        r'^https://www\.louisslutton\.com$',
        r'^https://.*\.vercel\.app$',
        r'^https://.*\.railway\.app$',
        r'^http://localhost:\d+$',  # For local development
    ]

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            headers = dict(scope.get("headers", []))
            origin = headers.get(b"origin", b"").decode()

            print(f"WebSocket connection attempt - Origin: {origin}, Path: {scope.get('path', '')}")

            # Check if origin matches any allowed pattern
            allowed = any(
                re.match(pattern, origin)
                for pattern in self.ALLOWED_ORIGIN_PATTERNS
            )

            if not allowed and origin:
                print(f"❌ WebSocket connection REJECTED from origin: {origin}")
                print(f"   Allowed patterns: {self.ALLOWED_ORIGIN_PATTERNS}")
                await send({
                    "type": "websocket.close",
                    "code": 403,
                })
                return
            else:
                print(f"✅ WebSocket connection ALLOWED from origin: {origin}")

        return await super().__call__(scope, receive, send)


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": OriginValidatorMiddleware(
        JWTAuthMiddleware(
            URLRouter(
                comments_routing.websocket_urlpatterns
            )
        )
    ),
})
