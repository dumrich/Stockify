from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from core.models import Stock, Watchlist
from rest_framework import serializers
class StockSerializer(serializers.ModelSerializer):
    """Serializer for stock model"""
    class Meta:
        model = Stock
        fields = '__all__'

class WatchlistSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Watchlist model"""
    class Meta:
        model = Watchlist
        fields = '__all__'
