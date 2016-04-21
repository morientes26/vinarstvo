# -*- coding: utf-8 -*-
from django.conf.urls import url

from views.product_views import *
from views.group_views import *
from views.order_views import *

urlpatterns = [
	# index page
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^change-language/$', LangChangeView.as_view(), name='language'),

	# product page for managing products
	url(r'^product/$', ListProducts.as_view(), name='list_products'),
	url(r'^product/create/$', CreateProduct.as_view(), name='create_product'),
	url(r'^product/detail/(?P<pk>\d+)/$', DetailProduct.as_view(), name='detail_product'),
	url(r'^product/edit/(?P<pk>\d+)/$', EditProduct.as_view(), name='edit_product'),
	url(r'^product/add/(?P<pk>\d+)/$', AddProduct.as_view(), name='add_product'),
	url(r'^product/remove/(?P<pk>\d+)/$', RemoveProduct.as_view(), name='remove_product'),
	url(r'^product/delete/(?P<pk>\d+)/$', DeleteProduct.as_view(), name='delete_product'),
	url(r'^product/import/$', ImportView.as_view(), name='import_products'),

	# group page for managing groups
	url(r'^group/$', ListGroups.as_view(), name='list_groups'),
	url(r'^group/create/$', CreateGroup.as_view(), name='create_group'),
	url(r'^group/edit/(?P<pk>\d+)/$', EditGroup.as_view(), name='edit_group'),
	url(r'^group/delete/(?P<pk>\d+)/$', DeleteGroup.as_view(), name='delete_group'),

	# order page for managing orders
	url(r'^order/$', ListOrders.as_view(), name='list_orders'),
	url(r'^backorder/$', ListBackOrders.as_view(), name='list_back_orders'),
	url(r'^order/create/$', CreateOrder.as_view(), name='create_order'),
	url(r'^order/edit/(?P<pk>\d+)/$', EditOrder.as_view(), name='edit_order'),
	url(r'^order/detail/(?P<pk>\d+)/$', DetailOrder.as_view(), name='detail_order'),
	url(r'^order/done/(?P<pk>\d+)/$', DoneOrder.as_view(), name='done_order'),
	url(r'^order/delete/(?P<pk>\d+)/$', DeleteOrder.as_view(), name='delete_order'),

	url(r'^product/upload/$', UploadPhoto.as_view(), name='upload_photo'),

]
