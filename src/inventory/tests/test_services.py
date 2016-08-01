# -*- coding: utf-8 -*-

from django.test import TestCase
import datetime
from inventory.service import InventoryService
from inventory.models import *


class InventoryServiceTestCase(TestCase):

    service = InventoryService()
    event = None
    group = None

    def setUp(self):
        self.group = Group.objects.create(name="white")
        p1 = Product.objects.create(code="0123", origin_name="perla", price=5.30, is_wine=True, is_new=True, active=False, group=self.group)
        p2 = Product.objects.create(code="2344", origin_name="perla 2", price=5.30, is_wine=True, is_new=False, active=True, group=self.group)
        Product.objects.create(code="2346", origin_name="perla 3", price=5.30, is_wine=True, is_new=True, active=False)
        Product.objects.create(code="1223", origin_name="perla 4", price=5.30, is_wine=True, is_new=True, active=True)
        listP = [p1, p2]
        self.event = Event.objects.create(name="test", date_from=datetime.datetime(2013, 2, 1), date_to=datetime.datetime(2016, 10, 11))
        self.event.products = listP
        self.event.save()
        order = Order.objects.create(customer_name="test", event=self.event)

    def test_get_new_products(self):
        products = self.service.get_new_products()
        self.assertTrue(products)
        self.assertEquals(products.count(), 3)

    def test_get_all_products_in_cart(self):
        products = self.service.get_all_products_in_cart()
        self.assertTrue(products)
        self.assertEquals(products.count(), 2)

    def test_get_actual_events(self):
        events = self.service.get_event()
        self.assertTrue(events)
        self.assertEquals(events.products.count(), 2)

    def test_get_all_products_in_event(self):
        event = Event.objects.filter(name="test")
        products = self.service.get_all_products_in_event(event[0], self.group.name)
        self.assertTrue(products)
        self.assertEquals(len(products), 2)
        self.assertEquals(event[0].products.count(), 2)

    def test_get_actual_orders_by_name(self):
        orders = self.service.get_actual_orders_by_name("test")
        self.assertTrue(orders)
        self.assertEquals(orders.count(), 1)
        self.assertEquals(orders[0].done, False)
        self.assertEquals(orders[0].customer_name, "test")


    def test_unit_price(self):
        product_1 = Product.objects.get(code="0123")
        product_1.price = 20
        product_1.size = 0
        # size is 0, get real price
        self.assertEqual(self.service.get_unit_price(product_1), 20)

        product_1.price = 20
        product_1.size = None
        # size is None, get real price
        self.assertEqual(self.service.get_unit_price(product_1), 20)

        product_1.price = 0
        product_1.size = 10
        self.assertEqual(self.service.get_unit_price(product_1), 0)

        product_1.price = 10
        product_1.size = 0.75
        self.assertEqual(self.service.get_unit_price(product_1), 13.33)

        product_1.price = 12
        product_1.size = 3
        self.assertEqual(self.service.get_unit_price(product_1), 4)
