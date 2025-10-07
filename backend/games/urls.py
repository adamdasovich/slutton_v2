from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameCategoryViewSet, GameViewSet, GameProgressViewSet, MemoryImagesViewSet

router = DefaultRouter()
router.register(r'categories', GameCategoryViewSet, basename='game-category')
router.register(r'games', GameViewSet, basename='game')
router.register(r'progress', GameProgressViewSet, basename='game-progress')
router.register(r'memory-images', MemoryImagesViewSet, basename='memory-images')

urlpatterns = [
    path('', include(router.urls)),
]
