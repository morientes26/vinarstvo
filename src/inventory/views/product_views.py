# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import translation
from inventory.forms import ProductForm, GroupForm, WineForm
from inventory.models import Product, Group, Wine
from sync.service import sync_products_from_file
from vanilla import CreateView, DeleteView, ListView, UpdateView, TemplateView, View, DetailView
from winelist.settings import BASE_DIR


# index page

class IndexView(TemplateView):
	template_name = "index.html"

	def get(self, request, *args, **kwargs):
		# synchronization all products from xml file
		sync_products_from_file(BASE_DIR + '/inventory/static/test-data/data.xml')
		return super(IndexView, self).get(request, args, kwargs)


# change language en/sk

class LangChangeView(TemplateView):
	def get(self, request):
		lang = 'en' if request.session[translation.LANGUAGE_SESSION_KEY] == 'sk' else 'sk'
		translation.activate(lang)
		request.session[translation.LANGUAGE_SESSION_KEY] = lang
		return redirect('index')


# products managment views

# class ManageProduct(CreateView):
# 	model = Wine
# 	form_class = WineForm
# 	template_name = 'inventory/manage_product_form.html'
# 	success_url = reverse_lazy('list_products')
#
# 	def get(self, request, *args, **kwargs):
# 		# self.object = self.get_object()
# 		# form = self.get_form(instance=self.object)
# 		return super(ManageProduct, self).get(request, args, kwargs)
#
# 	def post(self, request, *args, **kwargs):
# 		form = WineForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return self.form_valid(form)
# 		return self.form_invalid(form)


class ListProducts(ListView):
	model = Product
	queryset = Product.objects.all()


class DetailProduct(TemplateView):
	template_name = "inventory/product_detail.html"

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		wine = None
		try:
			product = get_object_or_404(Product, pk=kwargs['pk'])
			if product.is_wine:
				wine = Wine.objects.get(product=product)
				if wine:
					context['wine'] = wine

			context['product2'] = product
		except Product.DoesNotExist:
			print("Product not found")
			raise

		return render(request, self.template_name, context={'wine': wine, 'product': product})


class CreateProduct(CreateView):
	model = Product
	form_class = ProductForm
	success_url = reverse_lazy('list_products')


class EditProduct(UpdateView):
	model = Product
	form_class = ProductForm
	success_url = reverse_lazy('list_products')

	def form_valid(self, form):
		print(form)
		return super(EditProduct, self).form_valid(form)


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

