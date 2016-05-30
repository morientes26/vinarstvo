"""
Serializer for model Product
""" 
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from inventory.models import Product, Event, Order, Item


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializing the Product
    """
    class Meta:
        model = Product
        fields = "__all__"


class EventSerializer(serializers.Serializer):
    """
    Serializing the Event
    """
    id = serializers.Field()
    date_from = serializers.Field()
    date_to = serializers.Field()
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
		model = Event


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializing the Item
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    amount = serializers.Field()

    class Meta:
		model = Item


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializing the Order
    """
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = Order
        fields = "__all__"

