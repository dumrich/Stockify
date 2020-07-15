from rest_framework import generics, viewsets
from .serializers import StockSerializer, WatchlistSerializer
from core.models import Stock, Watchlist
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class StockCreate(generics.CreateAPIView):
    """Create Stock Objects"""
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

class WatchlistListCreate(generics.ListCreateAPIView):
    """Watchlist ViewSet to create, view, and update Watchlists"""
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()

class WatchlistUpdateRetriveDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()

