# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel


class Photo(models.Model):
    """
    Photo of product (vine, snack, drink...)
    """
    title = models.CharField(max_length=120, blank=True, help_text="titulok fotky")
    blob = models.BinaryField(blank=True)

    def __unicode__(self):
        return self.title


class Product(models.Model):
    """
    Basic product of inventory
    """

    # Sync attributes
    code = models.CharField(max_length=20, unique=True, help_text="kód tovaru (skladový)")
    origin_name = models.CharField(max_length=60, blank=False, help_text="hrubý názov tovaru (skladový)")
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="cena tovaru")
    is_new = models.BooleanField(default=True, blank=True, help_text="produkt bol prave synchrnonizovany")
    import_date = models.DateTimeField(default=timezone.now)

    # Other attributes
    active = models.BooleanField(default=False, blank=True, help_text="aktívne zobrazenie v tablete")
    name = models.CharField(max_length=120, blank=True, help_text="názov pre zobrazenie v tablete")
    description = models.TextField(blank=True, help_text="popis produktu")
    size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="objem/jednotka")
    is_wine = models.BooleanField(default=False, blank=True, help_text="je produkt vino")

    # Relations
    group = models.ForeignKey('Group', null=True, blank=True, help_text="skupina")
    photos = models.ManyToManyField(Photo, help_text="fotky produktu")

    # Functions
    def __unicode__(self):
        return self.code + " - " + self.origin_name + " - new: " + str(self.is_new) + " " + self.name


class Group(models.Model):
    """
    Group of product (vine, snack, drink...)
    """
    name = models.CharField(max_length=120, blank=False, help_text="názov skupiny")

    def __unicode__(self):
        return self.name


class Award(models.Model):
    """
    Award of product
    """
    name = models.CharField(max_length=20, unique=True, help_text="názov")
    photo = models.ForeignKey('Photo', blank=True, help_text="malá fotka medaily/ocenenia")

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

    # relations
    product = models.ForeignKey('Product', help_text="produkt")

    # attributes
    WINE_COLOR = (('RED', 'červené'), ('WHITE', 'biele'), ('ROSE', 'ružové'))
    color = models.CharField(max_length=5, choices=WINE_COLOR, blank=True, help_text="farba vína")

    year = models.IntegerField(null=True, help_text="ročník", blank=True)

    WINE_ATTRIBUTE = [('SV', 'Stolové víno'), ('AV', 'Akostné víno'), ('KV', 'Kabinetné víno'),
                      ('NZ', 'Neskorý zber'), ('VH', 'Výber z hrozna'), ('BV', 'Bobuľový výber'),
                      ('HV', 'Hrozienkový výber'), ('SV', 'Slamové víno'), ('LV', 'Ľadové víno'),
                      ('VC', 'Výber z cibéb')]
    attribute = models.CharField(max_length=5, blank=True, choices=WINE_ATTRIBUTE, help_text="prívlastok")

    locality = models.CharField(max_length=60, blank=True, help_text="lokalita")
    sugar_content = models.CharField(max_length=20, blank=True, help_text="cukornatost")
    alcohol = models.CharField(max_length=20, blank=True, help_text="alkohol")

    WINE_RESIDUAL = (('DY', 'suché'), ('HD', 'polosuché'), ('HS', 'polosladké'), ('SW', 'sladké'))
    sugar_residual = models.CharField(max_length=2, blank=True, choices=WINE_RESIDUAL, help_text="zbytkový cukor")

    acidity = models.CharField(max_length=20, blank=True, help_text="celkové kyseliny")
    awards = models.ManyToManyField(Award, blank=True, help_text="medaily/ocenenia")

    def __unicode__(self):
        return "product_id: " + str(self.product.id) + " " + self.color + " " + str(self.year) + " " + self.locality


class Event(models.Model):
    """
    Product testing event
    """
    name = models.CharField(max_length=20, unique=True, help_text = "názov akcie/ochutnavky")
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
    customer_name = models.CharField(max_length=60, blank=False, help_text="meno zákazníka alebo názov stola")
    event = models.ForeignKey('Event', blank=True, help_text="akcia / ochutnavka")
    items = models.ManyToManyField(Item, blank=True, help_text="vybrane produkty na akcii / ochutnavke")
    done = models.BooleanField(default=False, blank=False, help_text="vybavena objednavka")

    def __unicode__(self):
        return self.customer_name + " " + self.event.name + " " + str(self.items.__sizeof__())