"""CarSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.urls import re_path as url
from django.conf.urls.static import static
from django.views.generic import RedirectView

from bases.views import index, history, setting
from django.conf import settings

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^setting/', setting, name='setting'),
    url('admin/', admin.site.urls),
    url(r'^car/', include('car.urls')),
    url(r'^gps/', include('gps.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^history/', history, name='history'),
    url(r'^users/', include('users.urls')),
    url(r'^favicon\.ico$', favicon_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

