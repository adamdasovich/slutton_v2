from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TriviaViewSet

router = DefaultRouter()
router.register(r'', TriviaViewSet, basename='trivia')

urlpatterns = router.urls
