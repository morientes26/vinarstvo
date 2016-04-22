# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, BooleanField, CharField
from inventory.models import Product, Group, Wine, Order, Photo
import uuid


class ProductForm(ModelForm):
	is_new = BooleanField(widget=forms.HiddenInput(), label=None, initial=True)

	class Meta:
		model = Product
		fields = ['code', 'origin_name', 'price', 'active', 'name', 'description', 'is_wine', 'size', 'group']


class WineForm(ModelForm):
	class Meta:
		model = Wine
		fields = "__all__"
		exclude = ('product',)


class GroupForm(ModelForm):
	class Meta:
		model = Group
		fields = "__all__"


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = "__all__"
		exclude = ('items', 'done')


class PhotoForm(ModelForm):
	uuid = CharField(widget=forms.HiddenInput(), label=None, initial=uuid.uuid4())

	class Meta:
		model = Photo
		fields = "__all__"
