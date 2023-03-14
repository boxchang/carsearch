from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import os
import uuid

from CarSearch.settings.base import MEDIA_ROOT
from car.forms import FileUploadForm
from jobs.models import FileJob, JobStatus
import dbfread
from django.urls import reverse

def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    batch_no = uuid.uuid4().hex[:10]
    file_name = '{}.{}'.format(batch_no, ext)

    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return batch_no, file_path

def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            raw_file = form.cleaned_data.get("file")
            fileJob = FileJob()
            fileJob.file_type = "GPS"
            batch_no, file_path = handle_uploaded_file(raw_file)
            fileJob.batch_no = batch_no
            fileJob.file = file_path
            table = dbfread.DBF(MEDIA_ROOT+file_path)
            fileJob.count = len(table)
            fileJob.success = 0
            fileJob.status = JobStatus.objects.get(id=1)  # WAIT
            fileJob.create_by = User.objects.get(id=1)
            fileJob.save()
            return redirect(reverse('job_detail'))
    else:
        form = FileUploadForm()

    return render(request, 'gps/upload.html', locals())