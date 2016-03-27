from django.contrib import admin
from .models import Product, Photo, Group, Award, Item, Wine, Order, Event

admin.site.register({Product, Photo, Group, Award, Item, Wine, Order, Event})
