"""
Custom template helpers
"""
from django import template
from django.template.defaultfilters import stringfilter
from inventory.models import Item, Product

register = template.Library()


@register.filter
@stringfilter
def flag_check(value):
	yes = "Y"
	no = "N"

	if value:
		return yes
	else:
		return no


@register.filter
def is_choosen(product, items):
	for it in items.all():
		if isinstance(it, Item):
			if product == it.product:
				return "checked"
		if isinstance(it, Product):
			if product == it:
				return "checked"

	return ""


@register.filter
def get_amount(product, items):
	for it in items.all():
		if product == it.product:
			return it.amount
	return 0


