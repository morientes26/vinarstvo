"""
Custom template helpers
"""
from django import template
from django.template.defaultfilters import stringfilter

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
