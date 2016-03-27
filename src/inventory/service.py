"""
Service for inventory managment
"""

import logging

from models import Product

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
					datefmt='%m/%d/%Y %I:%M:%S %p',
					filename='../src/inventory/log/service.log',
					level=logging.DEBUG)


def get_new_products():
	products = Product.objects.filter(is_new=True)
	logging.info('get_new_products - fetching %s data', products.count())
	return products


def get_all_products_in_cart():
	products = Product.objects.all(active=True)
	logging.info('get_all_products_in_cart - fetching %s data', products.count())
	return products
