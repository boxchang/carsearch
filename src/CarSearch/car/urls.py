from django.urls import re_path as url

from car.views import upload

urlpatterns = [
    url(r'^upload/$', upload, name='upload'),
]