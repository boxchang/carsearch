from django.urls import re_path as url
from gps.views import upload, gps_data_update, gps_data_download

urlpatterns = [
    url(r'^gps_data_update/$', gps_data_update, name='gps_data_update'),
    url(r'^upload/$', upload, name='gps_upload'),
    url(r'^download/$', gps_data_download, name='gps_download'),

]