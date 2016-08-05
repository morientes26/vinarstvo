"""
Serializer for model Product
""" 
from rest_framework import serializers
from inventory.models import *
from inventory.service import InventoryService


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializing the Photo
    """

    class Meta:
        model = Photo
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):
    """
    Serializing the Award
    """
    photo = PhotoSerializer(read_only=True, many=False)

    class Meta:
        model = Award
        fields = "__all__"
        

class WineSerializer(serializers.ModelSerializer):
    """
    Serializing the Wine
    """

    class Meta:
        model = Wine
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializing the Group
    """
    image = PhotoSerializer(read_only=True, many=False)

    class Meta:
        model = Group
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializing the Product
    """
    wine = WineSerializer(read_only=True, many=False)
    group = GroupSerializer(read_only=True, many=False)
    photos = PhotoSerializer(read_only=True, many=False)
    awards = AwardSerializer(read_only=True, many=True)

    # custom field
    unit_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_unit_price(self, obj):
        service = InventoryService()
        return service.get_unit_price(obj)


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
    #event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = Order
        fields = "__all__"


