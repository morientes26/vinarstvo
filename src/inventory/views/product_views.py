# coding=utf-8

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import translation
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory.forms import ProductForm, WineForm, PhotoForm
from inventory.models import Product, Wine, Photo, Award
from sync.service import sync_products_from_file
from vanilla import DeleteView, ListView, TemplateView, View
from winelist.settings import BASE_DIR
from inventory.service import InventoryService

import logging

logger = logging.getLogger(__name__)


# Views for products management

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index_ng.html'

    def get(self, request, *args, **kwargs):
        logger.debug("IndexerView")
        return super(IndexView, self).get(request, args, kwargs)


# import products from xml
class ImportView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/product_import.html'

    def get(self, request):
        logger.debug("importing data")
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
        return redirect('index')


class ListProducts(LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.all().order_by('id')


class DetailProduct(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/product_detail.html'
    service = InventoryService()

    def get(self, request, *args, **kwargs):
        try:
            p_tuple = self.service.get_product_by_id(kwargs['pk'])
            logger.debug("detail proudct %s", p_tuple)
            return render(request, self.template_name, context={
                'wine': p_tuple.wine,
                'product': p_tuple.product
            })
        except Exception:
            raise Http404('product %s  has not been found.' % kwargs['pk'])


class CreateProduct(LoginRequiredMixin, View):
    template_name = 'inventory/product_create.html'
    service = InventoryService()

    def get(self, request):
        logging.debug('create product %s', request)
        return render(request, self.template_name, context={
            'product_form': ProductForm(),
            'wine_form': WineForm(),
            'photo_form': PhotoForm(),
        })

    def post(self, request):
        logging.debug('POST - create product')
        product_form = ProductForm(request.POST)
        wine_form = WineForm(request.POST)

        if all([product_form.is_valid(), wine_form.is_valid()]):
            product = product_form.save(commit=False)
            if product.is_wine:
                wine = wine_form.save()
                product.wine = wine

            logging.debug('saving wine %s', product)
            product.save()
            self.service.upload_photos(request, product)

            messages.add_message(request, messages.INFO, _("product_created"))
        else:
            print("valid error")

        return redirect('list_products')


class EditProduct(LoginRequiredMixin, View):
    template_name = 'inventory/product_create.html'
    service = InventoryService()

    def get(self, request, **kwargs):
        logging.debug('GET - edit product')
        wine_form = WineForm()
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product_form = ProductForm(instance=product)
        if product.is_wine:
            wine_form = WineForm(instance=product.wine)
        return render(request, self.template_name, context={'product_form': product_form, 'wine_form': wine_form})

    def post(self, request, **kwargs):
        logger.debug("POST - edit product %s", request)
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product_form = ProductForm(data=request.POST, instance=product)
        logger.debug("product %s", product_form)
        wine_form = WineForm(data=request.POST)

        if product.is_wine:
            wine_form = WineForm(data=request.POST, instance=product.wine)
            logger.debug("wine %s", wine_form)

        if product_form.is_valid():
            print('product_form valid')
            pcd = product_form.cleaned_data
            if pcd['is_wine']:
                if wine_form.is_valid():
                    print('wine_form valid')
                    wine = wine_form.save()
                    product = product_form.save(commit=False)
                    product.wine = wine
                    product.save()
                else:
                    print('wine_form not valid %s', wine_form.errors)
            else:
                product_form.save()

            self.service.upload_photos(request, product)

            messages.add_message(request, messages.INFO, _("product_edited"))

        for p in product_form.errors:
            print("error: "+p)
        for w in wine_form.errors:
            print("error: "+w)

        return redirect('list_products')


class UploadPhoto(LoginRequiredMixin, View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UploadPhoto, self).dispatch(*args, **kwargs)

    def post(self, request):
        logging.debug('upload file')
        photo = Photo.objects.create(title=request.POST['title'], blob=request.FILES['blob'], uuid=request.POST['uuid'])
        logging.debug('insert f')
        return HttpResponse('ok')

    # photo_form = PhotoForm(data=request.POST, files=request.FILES)
    # if photo_form.is_valid():
    #	photo_form.save()
    #	return HttpResponse('ok')
    # raise Exception('Cannot upload photo')


class AddProduct(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            logging.debug('add product to cart %s', request)
            # product = Product.objects.get(pk=kwargs['pk'])
            product = get_object_or_404(Product, pk=kwargs['pk'])
            product.active = True
            product.save()
            logging.debug('added product to cart %s', product)
            print(product)
        except Product.DoesNotExist:
            logging.error("Product not found %s", kwargs['pk'])
        return redirect('list_products')


class RemoveProduct(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            product = get_object_or_404(Product, pk=kwargs['pk'])
            product.active = False
            product.save()
            logging.debug('remove product from cart %s', product)
        except Product.DoesNotExist:
            logging.error("Product not found %s", kwargs['pk'])
        return redirect('list_products')


class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('list_products')
