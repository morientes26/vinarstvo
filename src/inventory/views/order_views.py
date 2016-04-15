# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
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

	def get_context_data(self, **kwargs):
		context = super(EditOrder, self).get_context_data(**kwargs)
		context['products'] = service.get_all_products_in_cart()
		context['items'] = self.object.items
		return context


class DoneOrder(TemplateView):
	
	def get(self, request, *args, **kwargs):
		service.done_order(kwargs['pk'])	
		messages.add_message(request, messages.INFO, _("order_done"))
		return redirect('list_orders')


class DeleteOrder(DeleteView):
	model = Order
	success_url = reverse_lazy('list_orders')


class DetailOrder(TemplateView):
	template_name = 'inventory/order_detail.html'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		order = get_object_or_404(Order, pk=kwargs['pk'])
		return render(request, self.template_name, context={'order': order})
