from django.urls import path, include
from rest_framework import routers
from .views import StockCreate, WatchlistUpdateRetriveDelete, WatchlistListCreate


urlpatterns = [
    path('', StockCreate.as_view(), name='home'),
    path('users/', include('users.urls')),
    path('watchlist/', WatchlistListCreate.as_view(), name='list_create'),
    path('watchlist/<int:pk>/', WatchlistUpdateRetriveDelete.as_view(), name='detail')

]
