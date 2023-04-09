from django.urls import re_path as url
from gps.views import upload, gps_data_update, download, delete, gps_photo_upload

urlpatterns = [
    url(r'^gps_data_update/$', gps_data_update, name='gps_data_update'),
    url(r'^gps_photo_upload/$', gps_photo_upload, name='gps_photo_upload'),
    url(r'^upload/$', upload, name='gps_upload'),
    url(r'^download/$', download, name='gps_download'),
    url(r'^delete/$', delete, name='gps_delete'),
]