# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel
from winelist.settings import MEDIA_URL, BASE_DIR

import uuid

class Photo(models.Model):
	"""
	Photo of product (vine, snack, drink...)
	"""

	blob = models.FileField(upload_to=BASE_DIR + "/inventory/static/data/", blank=True)
	uuid = models.CharField(max_length=36, blank=True, default='') #uuid.uuid4()

	class Meta:
		app_label = 'inventory'

	def __unicode__(self):
		return str(self.pk)+ " " +self.uuid


class Product(models.Model):
	"""
	Basic product of inventory
	"""

	# Sync attributes
	code = models.CharField(max_length=20, unique=True, help_text="kod tovaru (skladovy)")
	origin_name = models.CharField(max_length=60, blank=False, help_text="hruby nazov tovaru (skladovy)")
	price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="cena tovaru")
	is_new = models.BooleanField(default=True, blank=True, help_text="produkt bol prave synchrnonizovany")
	import_date = models.DateTimeField(default=timezone.now)

	# Other attributes
	active = models.BooleanField(default=False, blank=True, help_text="aktivne zobrazenie v tablete")
	name = models.CharField(max_length=120, blank=True, help_text="nazov pre zobrazenie v tablete")
	description = models.TextField(blank=True, help_text="popis produktu")
	size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="objem/jednotka")
	is_wine = models.BooleanField(default=False, blank=True, help_text="je produkt vino")

	# Relations
	group = models.ForeignKey('Group', null=True, blank=True, help_text="skupina")
	photos = models.ManyToManyField(Photo, help_text="fotky produktu", blank=True)
	wine = models.ForeignKey('Wine', null=True, blank=True, help_text="wine")

	#Overriding
	def save(self, *args, **kwargs):
		if self.name=="":
			self.name = self.origin_name
		super(Product, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.code + " - " + self.origin_name + " - new: " + str(self.is_new) + " " + self.name + " - is active: " + str(self.active) 


class Group(models.Model):
	"""
	Group of product (vine, snack, drink...)
	"""
	name = models.CharField(max_length=120, blank=False, help_text="nazov skupiny")

	def __unicode__(self):
		return self.name


class Award(models.Model):
	"""
	Award of product
	"""
	name = models.CharField(max_length=20, unique=True, help_text="nazov")
	photo = models.ForeignKey('Photo', blank=True, help_text="mala fotka medaily/ocenenia")

	def __unicode__(self):
		return self.name


class Specification(PolymorphicModel):
	"""
	Specification of product (vine, snack, drink...)
	"""
	code = models.CharField(max_length=20, help_text="kod typu produktu")
	name = models.CharField(max_length=120, help_text="nazov typu produktu")

	def __unicode__(self):
		return self.code + " - " + self.name


class Wine(models.Model):
	"""
	Additional attribute for product 'wine'
	"""

	# attributes
	WINE_COLOR = (('RED', 'cervene'), ('WHITE', 'biele'), ('ROSE', 'ruzove'))
	color = models.CharField(max_length=5, choices=WINE_COLOR, blank=True, help_text="farba vina")

	year = models.IntegerField(null=True, help_text="rocnik", blank=True, default="")

	WINE_ATTRIBUTE = [
		('SV', 'Stolove vino'),
		('AV', 'Akostne vino'),
		('KV', 'Kabinetne vino'),
		('NZ', 'Neskory zber'),
		('VH', 'Vyber z hrozna'),
		('BV', 'Bobulovy vyber'),
		('HV', 'Hrozienkovy vyber'),
		('SV', 'Slamove vino'),
		('LV', 'Ladove vino'),
		('VC', 'Vyber z cibeb')
	]
	attribute = models.CharField(max_length=5, blank=True, choices=WINE_ATTRIBUTE, help_text="privlastok")

	locality = models.CharField(max_length=60, blank=True, help_text="lokalita", default="")
	sugar_content = models.CharField(max_length=20, blank=True, help_text="cukornatost", default="")
	alcohol = models.CharField(max_length=20, blank=True, help_text="alkohol", default="")

	WINE_RESIDUAL = (('DY', 'suche'), ('HD', 'polosuche'), ('HS', 'polosladke'), ('SW', 'sladke'))
	sugar_residual = models.CharField(max_length=2, blank=True, choices=WINE_RESIDUAL, help_text="zbytkovy cukor")

	acidity = models.CharField(max_length=20, blank=True, help_text="celkove kyseliny", default="")
	awards = models.ManyToManyField(Award, blank=True, help_text="medaily/ocenenia")
	serving = models.CharField(max_length=255, blank=True, help_text="servirovanie", default="")

	def __unicode__(self):
		return "pk: " + str(self.pk) + " " + str(self.year)


class Event(models.Model):
	"""
	Product testing event
	"""
	name = models.CharField(max_length=20, unique=True, help_text="nazov akcie/ochutnavky")
	date_from = models.DateTimeField(blank=True, null=True, help_text="datum a cas zaciatku akcie")
	date_to = models.DateTimeField(blank=True, null=True, help_text="datum a cas konca akcie")
	products = models.ManyToManyField(Product, blank=True, help_text="vyber produktov na ochutnavke/akcii")

	def __unicode__(self):
		return self.name + " " + str(self.date_from) + " " + str(self.date_to) + " " + str(self.products.__sizeof__())


class Item(models.Model):
	"""
	Chosen product and amount of it
	"""
	product = models.ForeignKey('Product', blank=False, help_text="vybrany produkt")
	amount = models.IntegerField(blank=False, default=0, help_text="mnozstvo")

	def __unicode__(self):
		return self.product.name + " " + str(self.amount)


class Order(models.Model):
	"""
	Order of event
	"""
	customer_name = models.CharField(max_length=60, blank=False, default='', help_text="meno zakaznika alebo nazov stola")
	contact_detail = models.CharField(max_length=256, blank=False, default='', help_text="kontaktne informacie - adresa")
	phone = models.CharField(max_length=20, blank=False, default='', help_text="telefonny kontakt")
	email =	models.CharField(max_length=40, blank=True, null=True, help_text="emailovy kontakt") 
	event = models.ForeignKey('Event', blank=True, help_text="akcia / ochutnavka")
	items = models.ManyToManyField(Item, blank=True, help_text="vybrane produkty na akcii / ochutnavke")
	done = models.BooleanField(default=False, blank=False, help_text="vybavena objednavka")

	def __unicode__(self):
		return self.customer_name + " " + self.event.name + " " + str(self.items.__sizeof__())
