# -*- coding: utf-8 -*-

from django.test import TestCase
from sync.service import sync_products_from_file
from winelist.settings import BASE_DIR


class SynchronizationTestCase(TestCase):

    TEST_FILE = BASE_DIR + "/inventory/static/test-data/data.xml"

    def test_sync_products_from_file(self):
        """ Synchronization product from xml files """

        count = sync_products_from_file(self.TEST_FILE)
        self.assertEqual(count, 10, "count of imported product has to be 10")
