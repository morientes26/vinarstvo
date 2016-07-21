# -*- coding: utf-8 -*-
import os

from django.test import TestCase
from inventory.models import *
import inventory.utils
from winelist.settings import BASE_DIR


class ProductManageTestCase(TestCase):

    product = None
    product2 = None
    wine = None
    wine2 = None
    TEST_FILE = BASE_DIR + "/inventory/static/test-data/test.cache"

    def setUp(self):
        group = Group.objects.create(name="Skupina tekutiny")
        self.wine = Wine.objects.create(year=2012, attribute="SW",
                                        acidity="12.23 ph", locality="Tibava")
        self.product = Product.objects.create(wine=self.wine, code="0123", origin_name="Karpatska perla", price=5.30,
                                              is_wine=True, group=group)

        self.wine2 = Wine.objects.create(year=2015, attribute="DY",
                                         acidity="3.23 ph", locality="Velky Krtis")

        self.product2 = Product.objects.create(wine=self.wine2, code="4567", origin_name="Karpatska perla 2",
                                               price=2.34, is_wine=True)

        self.create_test_file()

    def tearDown(self):
        self.delete_test_file()

    def test_product_has_specification_wine(self):
        """ Find product and specification data """

        product = Product.objects.get(wine=self.wine)
        self.assertEqual(product.origin_name, "Karpatska perla")
        self.assertEqual(product.group.name, "Skupina tekutiny")
        self.assertEqual(product.wine.year, 2012)
        self.assertEqual(product.wine.attribute, "SW")
        self.assertEqual(product.wine.locality, "Tibava")

    def test_order_products(self):
        """ Ordering products """

        event = Event.objects.create(name="Ochutnavka c.1")
        product_1 = Product.objects.get(code="0123")
        product_2 = Product.objects.get(code="4567")
        item_1 = Item.objects.create(product=product_1, amount=10)
        item_2 = Item.objects.create(product=product_2, amount=3)
        order = Order.objects.create(customer_name="Stol c.1", event=event)
        order.items.add(item_1, item_2)
        order.save()
        order = Order.objects.get(customer_name="Stol c.1")
        self.assertEqual(order.event.name, "Ochutnavka c.1")
        self.assertEquals(order.items.count(), 2)

    def test_add_awards(self):
        """ Add awards to product """

        blob = inventory.utils.file_to_blob(self.TEST_FILE)
        photo = Photo.objects.create(blob=blob)
        award = Award.objects.create(name="Udelenie ceny c.1", photo=photo)
        self.wine.awards.add(award)
        self.wine.save()
        winetest = Wine.objects.get(pk=self.wine.id)
        self.assertEqual(winetest.awards.first().name, "Udelenie ceny c.1")

    def create_test_file(self):
        if not os.path.isfile(self.TEST_FILE):
            with open(self.TEST_FILE, 'w') as f:
                f.write('Hello, world!\n')

    def delete_test_file(self):
        if os.path.isfile(self.TEST_FILE):
            os.remove(self.TEST_FILE)
