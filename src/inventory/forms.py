from django import forms
from django.forms import ModelForm, BooleanField
from inventory.models import Product, Group, Wine


class ProductForm(ModelForm):
	is_new = BooleanField(widget=forms.HiddenInput(), label=None, initial=True)

	class Meta:
		model = Product
		fields = ['code', 'origin_name', 'price', 'active', 'name', 'description', 'is_wine', 'size', 'group']

	#FIXME: not working - cannot change value before save
	#def save(self, commit=False):
	#	instance = super(ProductForm, self).save(commit=False)
	#	instance.is_new = False
	#	print(instance)
	#	if commit:
	#		instance.save(commit=True)
	#	return instance


class WineForm(ModelForm):
	class Meta:
		model = Wine
		fields = "__all__"
		exclude = ('product',)


class GroupForm(ModelForm):
	class Meta:
		model = Group
		fields = "__all__"
