from django.urls import re_path as url

from users.views import *

urlpatterns = [
    url(r'^detail/$', detail, name='user_detail'),
    url(r'^user_edit/$', user_edit, name='user_edit'),
    url(r'^user_auth_api/$', user_auth_api, name='user_auth_api'),
    url(r'^postponed_expire_api/$', postponed_expire_api, name='postponed_expire_api'),
    url(r'^postpone_record_api/$', postpone_record_api, name='postpone_record_api'),
    url(r'^create/$', create, name='user_create'),
    url(r'^list/$', user_list, name='user_list'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
]