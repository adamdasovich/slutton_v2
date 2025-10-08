"""
URL configuration for slutton_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint for Railway"""
    return JsonResponse({"status": "ok", "service": "Louis Slutton Backend"})

urlpatterns = [
    path("", health_check, name="health_check"),  # Root health check
    path("health/", health_check, name="health"),  # /health endpoint
    path("admin/", admin.site.urls),
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/products/<slug:product_slug>/ratings/', include('ratings.urls')),
    path('api/products/<slug:product_slug>/comments/', include('comments.urls')),
    path('api/games/', include('games.urls')),
    path('api/trivia/', include('trivia.urls')),
]

# Serve media files in both development and production
# In production, these should eventually be moved to S3
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
