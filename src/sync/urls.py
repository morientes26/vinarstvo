from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
	# sync page
	url(r'^test1/$', views.product_sync),
	url(r'^test2/$', views.SyncView.as_view(), name='sync-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)