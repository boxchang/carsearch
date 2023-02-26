from django.urls import re_path as url
from jobs.views import detail

urlpatterns = [
    url(r'^detail/$', detail, name='job_detail'),
]