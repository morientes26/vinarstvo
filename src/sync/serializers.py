"""
Serializer for model Product
""" 
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
from inventory.models import Product
from rest_framework_xml.parsers import XMLParser

#import logging

#logger = logging.getLogger(__name__)

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializing all the Product
    """
    code = serializers.CharField(max_length=20)
    origin_name = serializers.CharField(max_length=60)
    price = serializers.FloatField()
    amount = serializers.IntegerField()
    class Meta:
        model = Product
    #    fields = ('code', 'origin_name', 'price', 'amount')


class ProductDeserializer:

    @staticmethod
    def parse(content):
        stream = BytesIO(content)
        data = XMLParser().parse(stream)
        #logger.debug('parsing data: %s', data)
        print('parsing data: %s', data)
        return data


