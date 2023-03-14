from django.conf import settings
from django.db import models
from django.utils import timezone
import os
import uuid



# Define user directory path
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class JobStatus(models.Model):
    status_en = models.CharField(max_length=50)
    status_cn = models.CharField(max_length=50)
    status_desc = models.TextField()
    create_at = models.DateTimeField(default=timezone.now)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='job_status_create_at')
    update_at = models.DateTimeField(default=timezone.now)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='job_status_update_at')

    def __str__(self):
        return self.status_cn


class FileJob(models.Model):
    batch_no = models.CharField(max_length=50, blank=False)
    file_type = models.CharField(max_length=50, blank=True)
    file = models.FileField(upload_to=user_directory_path, null=True)
    status = models.ForeignKey(
        JobStatus, related_name='job_status', on_delete=models.DO_NOTHING)
    count = models.IntegerField()
    success = models.IntegerField(default=0)
    start_time = models.CharField(max_length=50, blank=True)
    end_time = models.CharField(max_length=50, blank=True)
    exe_time = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='job_create_by')  # 建立者
