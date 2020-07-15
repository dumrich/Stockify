from core.models import Stock, Watchlist
from rest_framework import serializers
from django.contrib.auth import get_user_model

class StockSerializer(serializers.ModelSerializer):
    """Serializer for stock model"""
    class Meta:
        model = Stock
        fields = ['id','name']
        read_only_fields = ('id',)

class WatchlistSerializer(serializers.ModelSerializer):
    """Serializer for Watchlist model"""
    stock = serializers.PrimaryKeyRelatedField(many=True, queryset=Stock.objects.all(), allow_null=True)
    class Meta:
        model = Watchlist
        fields = ['id', 'stock', 'name', 'author']
        read_only_fields = ('id',)
