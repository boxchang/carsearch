from django.urls import re_path as url

from car.views import download
from gps.views import upload, gps_data_update

urlpatterns = [
    url(r'^gps_data_update/$', gps_data_update, name='gps_data_update'),
    url(r'^upload/$', upload, name='gps_upload'),
    url(r'^download/$', download, name='gps_download'),

]