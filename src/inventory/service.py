# -*- coding: utf-8 -*-
"""
Service for inventory managment
"""

import datetime
from collections import namedtuple
from inventory.models import *

import logging
logger = logging.getLogger(__name__)


class InventoryService:
	"""
	Service for getting information about products, orders, events
	"""

	def get_product_by_id(self, id):
		"""
		Args: id: product primary key
		Returns: tuples 'product' with keys product, wine
		Throws: Exception
		"""
		product = Product.objects.get(pk=id)
		if not product:
			logger.error("Product not found by pk =  ", id)
			raise Exception("Product not found")

		return product

	def get_products(self, group):
		"""
		Args: group - String of group name
		Returns: list of products
		"""
		if self._is_event(): # find if exist actual event
			logger.debug('finded actual event')
			event = self.get_actual_events(group)
			return self.get_all_products_in_event(event[0])
		else:
			logger.debug('not actual event')			
			return self.get_all_products_in_cart(group)

	def upload_photos(self, request, product):
		if request.FILES:
			for file in request.FILES:
				if file == 'photo_upload':
					photo = Photo.objects.create(blob=file)
					product.photos.add(photo)
					logger.debug('upload file and create photo %s ', photo)
				if file == 'award_upload':
					a_photo = Photo.objects.create(blob=file)
					logger.debug('upload file and create photo %s ', a_photo)
					award = Award.objects.create(name=a_photo.uuid, photo=a_photo)
					wine.awards.add(award)
					wine.save() 

	def get_new_products(self):
		products = Product.objects.filter(is_new=True)
		logger.debug('get_new_products - fetching %s data', products.count())
		return products

	def get_all_products_in_cart(self, group):
		grp = Group.objects.filter(name=group)
		products = Product.objects.filter(active=True, group=grp)
		logger.debug('get_all_products_in_cart - fetching %s data', products.count())
		return products

	def get_all_products_in_event(self, event):
		if event:
			if hasattr(event, 'products'):
				print('has products')
				products = event.products
				logger.debug('get_all_products_in_event from %s - fetching %s data', event, products.count())
				return products
		return None

	def get_actual_events(self, group):
		now = datetime.datetime.now()
		events = Event.objects.filter(date_from__lte=now, date_to__gte=now, products__group__name=group).order_by('id')
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

	def _is_event(self):
		now = datetime.datetime.now()
		events = Event.objects.filter(date_from__lte=now, date_to__gte=now)
		print(events)
		logger.debug('active event %s', events.count())
		if events:
			return True
		return False


# ------------------------------------------------------------------------------------ order --------
	"""@deprecated"""
	def create_order(self, customer_name, event_id, product_list):
		event = Event.objects.get(pk=event_id)		
		items = Product.objects.filter(pk__in=product_list)
		if event==None or items==None:
			raise ValueError('input parameters are bad')
		order = Order.objects.create(customer_name=customer_name, event=event, items=items)
		return order

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
