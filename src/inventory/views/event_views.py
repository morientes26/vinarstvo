# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory.forms import EventForm
from inventory.models import Event, Item, Product
from vanilla import CreateView, DeleteView, ListView, UpdateView
from inventory.service import InventoryService

import logging
logger = logging.getLogger(__name__)
service = InventoryService()

# Views for groups management

class EventView(LoginRequiredMixin):
	def process_form(self, request, form):
		items = []
		for field in request.POST:
			if field.startswith('p_'):
				id = request.POST[field]
				p = Product.objects.get(pk=id)
				items.append(p)

		if form.is_valid():
			self.object = form.save()
			self.object.products = []
			self.object.products.add(*items)
			self.object.save()
			return True
		return False

	def prepare_form(self, context):
		context['products'] = service.get_all_products_in_cart()
		if hasattr(self, 'object'):
			context['items'] = self.object.products
		return context


class ListEvents(LoginRequiredMixin, ListView):
	model = Event
	queryset = Event.objects.all()


class CreateEvent(EventView, CreateView):
	model = Event
	form_class = EventForm
	success_url = reverse_lazy('list_events')

	def get_context_data(self, **kwargs):
		return self.prepare_form(super(CreateEvent, self).get_context_data(**kwargs))

	def post(self, request, *args, **kwargs):
			form = self.get_form(data=request.POST)
			if self.process_form(request, form):
				return HttpResponseRedirect(self.get_success_url())

			return self.form_invalid(form)


class EditEvent(EventView, UpdateView):
	model = Event
	form_class = EventForm
	success_url = reverse_lazy('list_events')

	def get_context_data(self, **kwargs):
		return self.prepare_form(super(EditEvent, self).get_context_data(**kwargs))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form(data=request.POST, instance=self.object)

		if self.process_form(request, form):
			return HttpResponseRedirect(self.get_success_url())

		return self.form_invalid(form)


class DeleteEvent(LoginRequiredMixin, DeleteView):
	model = Event
	success_url = reverse_lazy('list_events')

