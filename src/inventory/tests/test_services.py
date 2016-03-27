# -*- coding: utf-8 -*-

from django.test import TestCase
from inventory import service
from inventory.models import Product


class InventoryServiceTestCase(TestCase):

    def setUp(self):
        Product.objects.create(code="0123", origin_name="perla", price=5.30, is_wine=True, is_new=True, active=False)
        Product.objects.create(code="2344", origin_name="perla 2", price=5.30, is_wine=True, is_new=False, active=True)
        Product.objects.create(code="2346", origin_name="perla 3", price=5.30, is_wine=True, is_new=True, active=False)
        Product.objects.create(code="1223", origin_name="perla 4", price=5.30, is_wine=True, is_new=True, active=True)

    def test_get_new_products(self):
        products = service.get_new_products()
        self.assertTrue(products)
        self.assertEquals(products.count(), 3)

    def test_get_all_products_in_cart(self):
        products = service.get_all_products_in_cart()
        self.assertTrue(products)
        self.assertEquals(products.count(), 2)
