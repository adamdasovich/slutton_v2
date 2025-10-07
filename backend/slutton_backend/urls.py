"""
URL configuration for slutton_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
