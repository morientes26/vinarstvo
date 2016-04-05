# coding=utf-8

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import translation
from inventory.forms import ProductForm, WineForm
from inventory.models import Product, Wine
from sync.service import sync_products_from_file
from vanilla import DeleteView, ListView, TemplateView, View
from winelist.settings import BASE_DIR

import logging
logger = logging.getLogger(__name__)

# Views for products management

class IndexView(TemplateView):

	template_name = 'index.html'

	def get(self, request, *args, **kwargs):
		logger.debug("this is a debug message!")
		return super(IndexView, self).get(request, args, kwargs)


# import products from xml

class ImportView(TemplateView):
	template_name = 'inventory/product_import.html'

	def get(self, request, *args, **kwargs):
		# synchronization all products from xml file
		import_count = sync_products_from_file(BASE_DIR + '/inventory/static/test-data/data.xml')
		context = self.get_context_data()
		context['import_count'] = import_count
		return self.render_to_response(context)


# change language en/sk

class LangChangeView(TemplateView):

	def get(self, request, *args, **kwargs):
		lang = 'en'
		if translation.LANGUAGE_SESSION_KEY in request.session:
			lang = 'en' if request.session[translation.LANGUAGE_SESSION_KEY] == 'sk' else 'sk'
			translation.activate(lang)
			request.session[translation.LANGUAGE_SESSION_KEY] = lang
		else:
			request.session[translation.LANGUAGE_SESSION_KEY] = lang
		return redirect('index')


class ListProducts(ListView):
	model = Product
	queryset = Product.objects.all()


class DetailProduct(TemplateView):
	template_name = 'inventory/product_detail.html'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		wine = None
		try:
			id = kwargs['pk']
			logger.debug("id = " + str(id))
			product = get_object_or_404(Product, pk=id)
			logger.debug("product = " + str(product.id))
			if product.is_wine:
				logger.debug("product is wine")
				wine = Wine.objects.filter(product=product)
				if wine:
					logger.debug("wine is for product [id]" + str(product.id))
					context['wine'] = wine

		except Product.DoesNotExist:
			print("Product not found")
			raise

		return render(request, self.template_name, context={'wine': wine, 'product': product})


class CreateProduct(View):

	template_name = 'inventory/product_create.html'

	def get(self, request):
		product_form = ProductForm()
		wine_form = WineForm()
		return render(request, self.template_name, context={'product_form': product_form, 'wine_form': wine_form})

	def post(self, request):
		product_form = ProductForm(request.POST)
		wine_form = WineForm(request.POST)
		if all([product_form.is_valid(), wine_form.is_valid()]):
			print("all valid")
			product = product_form.save()
			if product.is_wine:
				wine = wine_form.save(commit=False)
				wine.product = product
				wine.save()
		return redirect('list_products')


class EditProduct(View):

	template_name = 'inventory/product_create.html'

	def get(self, request, **kwargs):
		wine_form = WineForm()
		product = get_object_or_404(Product, pk=kwargs['pk'])
		product_form = ProductForm(instance=product)
		if product.is_wine:
			wine = Wine.objects.get(product=product)
			if wine:
				wine_form = WineForm(instance=wine)
		return render(request, self.template_name, context={'product_form': product_form, 'wine_form': wine_form})

	def post(self, request, **kwargs):
		product = get_object_or_404(Product, pk=kwargs['pk'])
		product_form = ProductForm(data=request.POST, instance=product)
		wine_form = WineForm(data=request.POST)
		if product.is_wine:
			wine = Wine.objects.get(product=product)
			wine_form = WineForm(data=request.POST, instance=wine)

		if product_form.is_valid():
			pcd = product_form.cleaned_data
			if pcd['is_wine']:
				if wine_form.is_valid():
					product = product_form.save()
					wine = wine_form.save(commit=False)
					wine.product = product
					wine.save()

			else:
				product_form.save()

		for p in product_form.errors:
			print(p)
		return redirect('list_products')


class AddProduct(TemplateView):

	def get(self, request, *args, **kwargs):
		try:
			product = get_object_or_404(Product, pk=kwargs['pk'])
			product.active = True
			product.save()
		except Product.DoesNotExist:
			print("Product not found", id)
		return redirect('list_products')


class RemoveProduct(TemplateView):
	def get(self, request, *args, **kwargs):
		try:
			product = get_object_or_404(Product, pk=kwargs['pk'])
			product.active = False
			product.save()
		except Product.DoesNotExist:
			print("Product not found", id)
		return redirect('list_products')


class DeleteProduct(DeleteView):
	model = Product
	success_url = reverse_lazy('list_products')

