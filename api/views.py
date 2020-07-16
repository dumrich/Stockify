from rest_framework import generics, permissions
from .serializers import StockSerializer, WatchlistSerializer
from core.models import Stock, Watchlist
from .permissions import IsOwnerOrReadOnly

class StockCreate(generics.CreateAPIView):
    """Create Stock Objects"""
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

class WatchlistListCreate(generics.ListCreateAPIView):
    """Watchlist ViewSet to create, view, and update Watchlists"""
    serializer_class = WatchlistSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Watchlist.objects.filter(author=user)

class WatchlistUpdateRetriveDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        user=self.request.user
        return Watchlist.objects.filter(author=user)
