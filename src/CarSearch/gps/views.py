from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from CarSearch.settings.base import MEDIA_ROOT
from bases.utils import FileUploadJob
from car.forms import FileUploadForm
from jobs.models import FileJob, JobStatus
import dbfread
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            raw_file = form.cleaned_data.get("file")
            fileJob = FileJob()
            fileJob.file_type = "GPS"
            batch_no, file_path = FileUploadJob().handle_uploaded_file(raw_file)
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