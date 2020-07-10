from rest_framework import generics, viewsets
from .serializers import StockSerializer, WatchlistSerializer
from core.models import Stock, Watchlist

class StockCreate(generics.CreateAPIView):
    """Create Stock Objects"""
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

class WatchlistViewSet(viewsets.ModelViewSet):
    """Watchlist ViewSet to create, view, and update Watchlists"""
    serializer_class = WatchlistSerializer

    def get_queryset(self):
        return Watchlist.objects.all()

