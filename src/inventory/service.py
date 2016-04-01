"""
Service for inventory managment
"""

import logging
import datetime

from inventory.models import Product, Event, Order


class InventoryService:
	"""
	Service for getting information about products, orders, events
	"""

	logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
					datefmt='%m/%d/%Y %I:%M:%S %p',
					filename='../src/inventory/log/service.log',
					level=logging.DEBUG)


	def get_new_products(self):
		products = Product.objects.filter(is_new=True)
		logging.info('get_new_products - fetching %s data', products.count())
		return products


	def get_all_products_in_cart(self):
		products = Product.objects.filter(active=True)
		logging.info('get_all_products_in_cart - fetching %s data', products.count())
		return products


	def get_actual_events(self):
		now = datetime.datetime.now()
		events = Event.objects.filter(date_from__lte=now, date_to__gte=now)
		logging.info('get_actual_events - fetching %s data', events.count())
		return events


	def get_actual_orders_by_name(self, name):
		orders = Order.objects.filter(done=False)
		logging.info('get_actual_orders_by_name - fetching %s data', orders.count())
		return orders
