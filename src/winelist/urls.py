"""
Base Winelist URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^sync/', include('sync.urls')),
]
