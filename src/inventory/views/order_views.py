# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from inventory.forms import OrderForm
from inventory.models import Order
from vanilla import CreateView, DeleteView, ListView, UpdateView, TemplateView
from inventory.service import InventoryService

import logging
logger = logging.getLogger(__name__)
service = InventoryService()

# Views for groups management

class ListOrders(ListView):
	model = Order
	queryset = Order.objects.all()


class ListBackOrders(ListView):
	model = Order
	queryset = service.get_all_back_orders()


class CreateOrder(CreateView):
	model = Order
	form_class = OrderForm
	success_url = reverse_lazy('list_orders')


class EditOrder(UpdateView):
	model = Order
	form_class = OrderForm
	success_url = reverse_lazy('list_orders')


class DoneOrder(TemplateView):
	def get(self, request, *args, **kwargs):
		service.done_order(kwargs['pk'])	
		#TODO: message - order has been done
		return redirect('list_orders')


class DeleteOrder(DeleteView):
	model = Order
	success_url = reverse_lazy('list_orders')


class DetailOrder(TemplateView):
	template_name = 'inventory/order_detail.html'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		try:
			id = kwargs['pk']
			logger.debug("id = " + str(id))
			order = get_object_or_404(Order, pk=id)
			logger.debug("order = " + str(order.id))			

		except Order.DoesNotExist:
			print("Order not found")
			raise

		return render(request, self.template_name, context={'order': order})
