# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from winelist.settings import MEDIA_ROOT, MEDIA_URL
from views.cart_views import *
from views.product_views import *
from views.group_views import *
from views.order_views import *
from views.event_views import *
from views.access_views import *
from views.setting_views import *
from views.api_views import *

urlpatterns = [
	# authorization
	url(r'^accounts/login/$', auth_views.login, {'template_name': 'access/login.html'}),
	url(r'^accounts/profile/', login_view,name='login'),
	url(r'^accounts/logout/', logout_view, name='logout'),

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
	url(r'^order/edit/(?P<pk>\d+)/$', EditOrder.as_view(), name='edit_order'),
	url(r'^order/detail/(?P<pk>\d+)/$', DetailOrder.as_view(), name='detail_order'),
	url(r'^order/done/(?P<pk>\d+)/$', DoneOrder.as_view(), name='done_order'),
	url(r'^order/delete/(?P<pk>\d+)/$', DeleteOrder.as_view(), name='delete_order'),

	# event page for managing events
	url(r'^event/$', ListEvents.as_view(), name='list_events'),
	url(r'^event/create/$', CreateEvent.as_view(), name='create_event'),
	url(r'^event/edit/(?P<pk>\d+)/$', EditEvent.as_view(), name='edit_event'),
	url(r'^event/delete/(?P<pk>\d+)/$', DeleteEvent.as_view(), name='delete_event'),

	# setting page for managing setting
	url(r'^setting/$', ListUserPreferences.as_view(), name='list_userpreferences'),
	url(r'^setting/edit/(?P<pk>\d+)/$', EditUserPreference.as_view(), name='edit_userpreference'),
	url(r'^setting/delete/(?P<pk>\d+)/$', DeleteUserPreference.as_view(), name='delete_userpreference'),

	url(r'^product/upload/$', UploadPhoto.as_view(), name='upload_photo'),

	url(r'^api/info/$', ApiInfoView.as_view(), name='api_info'),
	url(r'^api/products/$', get_products, name='api_product'),
	url(r'^api/product/list/$', get_product_from_primary_cart, name='api_product_list'),
	url(r'^api/product/event/list/$', get_product_from_actual_event, name='api_product_event_list'),
	url(r'^api/product/event/$', get_actual_event, name='api_get_actual_event'),
	url(r'^api/product/(?P<pk>\d+)/$', get_product_by_id, name='api_product'),
	url(r'^api/order/create/$', create_order, name='api_create_order'),
	url(r'^api/groups/$', get_groups, name='api_group_list'),
	url(r'^api/group/(?P<name>\w+)/$', get_group_by_name, name='api_group'),

	url(r'^cart/$', CartView.as_view(), name='cart_view'),
    url(r'^cart/(?P<token>\w+)/$', CartView.as_view(), name='cart_view'),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
