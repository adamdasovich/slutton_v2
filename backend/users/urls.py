from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-age/', views.verify_age, name='verify-age'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
]
