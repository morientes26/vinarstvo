"""
Serializer for model Product
""" 
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
from inventory.models import Product
from rest_framework_xml.parsers import XMLParser


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializing all the Product
    """
    class Meta:
        model = Product
        fields = ('code', 'origin_name', 'price')


class ProductDeserializer:

    @staticmethod
    def parse(content):
        stream = BytesIO(content)
        data = XMLParser().parse(stream)
        print(data)
        return data


