from django.urls import re_path as url

from car.views import upload, search, detail, car_data_update, download

urlpatterns = [
    url(r'^car_data_update/$', car_data_update, name='car_data_update'),
    url(r'^upload/$', upload, name='car_upload'),
    url(r'^download/$', download, name='car_download'),
    url(r'^detail/(?P<pk>.+)/$', detail, name='car_detail'),
    url(r'^search/$', search, name='car_search'),
]