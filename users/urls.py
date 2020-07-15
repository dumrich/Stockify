from django.urls import path
from rest_framework import routers
from .views import CreateUserView, CreateTokenView

urlpatterns = [
    path('', CreateUserView.as_view(), name='Create User'),
    path('login/', CreateTokenView.as_view(), name='api_token_auth')
]
