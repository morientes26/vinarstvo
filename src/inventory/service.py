"""
Service for inventory managment
"""

import datetime

from inventory.models import Product, Event, Order


import logging
logger = logging.getLogger(__name__)


class InventoryService:
	"""
	Service for getting information about products, orders, events
	"""

	def get_new_products(self):
		products = Product.objects.filter(is_new=True)
		logger.debug('get_new_products - fetching %s data', products.count())
		return products

	def get_all_products_in_cart(self):
		products = Product.objects.filter(active=True)
		logger.debug('get_all_products_in_cart - fetching %s data', products.count())
		return products

	def get_actual_events(self):
		now = datetime.datetime.now()
		events = Event.objects.filter(date_from__lte=now, date_to__gte=now)
		logger.debug('get_actual_events - fetching %s data', events.count())
		return events

	def get_actual_orders_by_name(self, customer_name):
		orders = Order.objects.filter(done=False, customer_name=customer_name)
		logger.debug('get_actual_orders_by_name - fetching %s data', orders.count())
		return orders

	def get_all_back_orders(self):
		""" get all not competed orders """
		orders = Order.objects.filter(done=False)
		logger.debug('get_all_back_orders - fetching %s data', orders.count())
		return orders

	def done_order(self, id):
		try:
			order = Order.objects.get(pk=id)
			order.done = True
			order.save()
			logger.debug('done_order - fetching %s data', order)
		except Product.DoesNotExist:
			logger.error("Order not found")
			raise	
		return order
