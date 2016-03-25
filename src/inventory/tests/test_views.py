# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import activate


class InventoryViewTestCase(TestCase):
    def setUp(self):
        pass

    def test_index(self):
        """ index page """
        response = self.client.get("/inventory/")
        self.assertTemplateUsed(response, "index.html")

    # def test_setting_localization(self):
    #     """ set localization """
    #     activate('en')
    #     response = self.client.get("/inventory/")
    #     self.assertTemplateUsed(response, "index.html")

    # def test_internationalization(self):
    #     for lang, h1_text in [('en', 'Inventory'),
    #                           ('sk', 'Inventár')]:
    #         activate(lang)
    #         self.client.get("inventory")
    #         h1 = self.client.find_element_by_tag_name("h1")
    #         self.assertEqual(h1.text, h1_text)

