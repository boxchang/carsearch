from django.urls import re_path as url

from gps.views import upload

urlpatterns = [
    url(r'^upload/$', upload, name='gps_upload'),
]