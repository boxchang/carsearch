from django.http import HttpResponse
from django.shortcuts import render, redirect
from bases.utils import downloadDbfFile
from CarSearch.settings.base import MEDIA_ROOT, GPS_FILE_ROOT
from bases.utils import FileUploadJob
from car.forms import FileUploadForm
from gps.forms import FileDownloadForm
from jobs.models import FileJob, JobStatus
import dbfread
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import threading
from tasks.gps_upload import GPS_Upload
from users.models import CustomUser
import os


@login_required
def gps_data_update(request):
    upload_form = FileUploadForm()
    download_form = FileDownloadForm()
    return render(request, 'gps/data_update.html', locals())


@login_required
def delete(request):
    upload_form = FileUploadForm()
    download_form = FileDownloadForm()
    return render(request, 'gps/data_update.html', locals())


@login_required
def download(request):
    if request.method == 'POST':
        sql = "select * from gps_gps"
        file_name = GPS_FILE_ROOT + 'gps_temp.dbf'
        downloadDbfFile(file_name , sql)
        with open(file_name, "rb") as fprb:
            response = HttpResponse(fprb.read(), content_type='application/x-dbf')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
        os.remove(file_name)
        return response


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
            fileJob.create_by = CustomUser.objects.get(id=1)
            fileJob.save()

            t = threading.Thread(target=run_upload)
            t.setDaemon(True)  # 主線程不管子線程的結果
            t.start()

            return redirect(reverse('job_detail'))
    else:
        form = FileUploadForm()

    return render(request, 'gps/data_update.html', locals())


def run_upload():
    obj = GPS_Upload()
    obj.execute()
