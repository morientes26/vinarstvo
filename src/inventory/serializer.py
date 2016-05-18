"""
Serializer for model Product
""" 
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializing all the Product
    """
    class Meta:
        model = Product
        fields = "__all__"
