from django.urls import path
from .views import RegisterAPI, AllUsers, PasswordAPI,UserPasswordAPI
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.core.cache import cache
urlpatterns = [
    path('register/', RegisterAPI.as_view(), name="registration"),
    path('password/', PasswordAPI.as_view()),
    path('all-password/', UserPasswordAPI.as_view()),
    path('users/', cache_page(60 * 15)(AllUsers.as_view())),
    path('token/', cache_page(60 * 15)(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('token/refresh/', cache_page(60 * 15)(TokenRefreshView.as_view()), name='token_refresh'),
]
