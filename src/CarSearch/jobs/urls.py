from django.urls import re_path as url
from jobs.views import detail, delete

urlpatterns = [
    url(r'^detail/$', detail, name='job_detail'),
    url(r'^delete/(?P<batch_no>\w+)/$', delete, name='job_delete'),
]