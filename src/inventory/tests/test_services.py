# -*- coding: utf-8 -*-

from django.test import TestCase
import datetime
from inventory.service import InventoryService
from inventory.models import Product, Event, Order


class InventoryServiceTestCase(TestCase):

    service = InventoryService()

    def setUp(self):
        p1 = Product.objects.create(code="0123", origin_name="perla", price=5.30, is_wine=True, is_new=True, active=False)
        p2 = Product.objects.create(code="2344", origin_name="perla 2", price=5.30, is_wine=True, is_new=False, active=True)
        Product.objects.create(code="2346", origin_name="perla 3", price=5.30, is_wine=True, is_new=True, active=False)
        Product.objects.create(code="1223", origin_name="perla 4", price=5.30, is_wine=True, is_new=True, active=True)
        listP = [p1, p2]
        event = Event.objects.create(name="test", date_from=datetime.datetime(2013, 2, 1), date_to=datetime.datetime(2016, 10, 11))
        event.products = listP
        event.save()
        order = Order.objects.create(customer_name="test", event=event)

    def test_get_new_products(self):
        products = self.service.get_new_products()
        self.assertTrue(products)
        self.assertEquals(products.count(), 3)

    def test_get_all_products_in_cart(self):
        products = self.service.get_all_products_in_cart()
        self.assertTrue(products)
        self.assertEquals(products.count(), 2)

    def test_get_actual_events(self):
        events = self.service.get_actual_events()
        self.assertTrue(events)
        self.assertEquals(events.count(), 1)
        self.assertEquals(events[0].products.count(), 2)

    def test_get_all_products_in_event(self):
        event = Event.objects.filter(name="test")
        products = self.service.get_all_products_in_event(event[0])
        self.assertTrue(products)
        self.assertEquals(products.count(), 2)
        self.assertEquals(event[0].products.count(), 2)

    def test_get_actual_orders_by_name(self):
        orders = self.service.get_actual_orders_by_name("test")
        self.assertTrue(orders)
        self.assertEquals(orders.count(), 1)
        self.assertEquals(orders[0].done, False)
        self.assertEquals(orders[0].customer_name, "test")

    def test_create_order(self):
        event = Event.objects.filter(name="test")
        order = self.service.create_order("objednavka", event.id, event.products)
        self.assertTrue(order)
        self.assertEquals(orders.customer_name, "objednavka")
