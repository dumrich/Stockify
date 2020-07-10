from django.urls import path
from rest_framework import routers
from .views import StockCreate, WatchlistViewSet

router = routers.SimpleRouter()

router.register(r'watchlist', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('', StockCreate.as_view(), name='home'),
]
urlpatterns += router.urls
