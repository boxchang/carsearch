from django.urls import re_path as url

from car.views import upload, search, detail

urlpatterns = [
    url(r'^upload/$', upload, name='car_upload'),
    url(r'^detail/(?P<pk>.+)/$', detail, name='car_detail'),
    url(r'^search/$', search, name='car_search'),
]