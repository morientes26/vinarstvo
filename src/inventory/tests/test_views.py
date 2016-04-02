# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.translation import activate
from inventory.forms import ProductForm
from inventory.models import Product
from inventory.views.product_views import DetailProduct


class InventoryViewTestCase(TestCase):

    ID = "1"
    factory = None

    def setUp(self):
        self.product = Product.objects.create(code="0123", origin_name="Karpatska perla", price=5.30, is_wine=True)
        self.ID = str(self.product.id)
        self.factory = RequestFactory()


    def test_index(self):
        """ index page """
        response = self.client.get("/inventory/")
        self.assertTemplateUsed(response, "index.html")

    def  test_change_language(self):
        """ test change language sk, en """
        response = self.client.get("/inventory/change-language/")
        self.assertEquals(response.status_code, 302)

    def test_import(self):
        """ test import product """
        response = self.client.get("/inventory/product/import/")
        self.assertTemplateUsed(response, "inventory/product_import.html")

    def test_setting_localization(self):
        """ set localization """
        response = self.client.get("/inventory/change-language")
        self.assertEquals(response.status_code, 301)

    def test_list_products(self):
        """ list of products """
        response = self.client.get("/inventory/product/")
        self.assertTemplateUsed(response, "inventory/product_list.html")

    def test_detail_product(self):
        """ detail of one product """
        response = self.client.get("/inventory/product/detail/" + self.ID)
        self.assertEquals(response.status_code, 301)

    def test_create_product(self):
        """ create product """
        response = self.client.get("/inventory/product/create/")
        self.assertTemplateUsed(response, "inventory/product_create.html")
        self.assertIsInstance(response.context['product_form'], ProductForm)

    def test_edit_product(self):
        """ edit product """
        response = self.client.get("/inventory/product/edit/" + self.ID)
        self.assertEquals(response.status_code, 301)

    def test_add_product(self):
        """ add product to wine cart """
        response = self.client.get("/inventory/product/add/" + self.ID)
        self.assertEquals(response.status_code, 301)

    def test_remove_product(self):
        """ remove product from wine cart """
        response = self.client.get("/inventory/product/remove/" + self.ID)
        self.assertEquals(response.status_code, 301)

    def test_delete_product(self):
        """ delete product """
        response = self.client.get("/inventory/product/delete/" + self.ID)
        self.assertEquals(response.status_code, 301)