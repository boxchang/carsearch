import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from bases.utils import MakeGPSDbfFile, unzip_file
from CarSearch.settings.base import MEDIA_ROOT, GPS_FILE_ROOT
from bases.utils import FileUploadJob
from car.forms import FileUploadForm
from gps.forms import FileDownloadForm, PhotoUploadForm
from gps.models import GPS
from jobs.models import FileJob, JobStatus
import dbfread
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import threading
from tasks.gps_upload import GPS_Upload
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
    if request.method == 'POST':
        try:
            sales = request.POST.get('sales')
            data_date_start = request.POST.get('data_date_start')
            data_date_end = request.POST.get('data_date_end')
            data = GPS.objects.filter(SALES_2=sales, DATE_2__range=(data_date_start, data_date_end))
            if data.all().count() > 0:
                data.delete()
                delete_result = True
            else:
                delete_result = None
        except:
            delete_result = False
    return render(request, 'gps/data_update.html', locals())


@login_required
def download(request):
    if request.method == 'POST':
        sales = request.POST.get('sales')
        data_date_start = request.POST.get('data_date_start')
        data_date_end = request.POST.get('data_date_end')
        sql = "select * from gps_gps where SALES_2 = '{SALES_2}' AND DATE_2 BETWEEN '{data_date_start}' AND '{data_date_end}'"\
            .format(SALES_2=sales, data_date_start=data_date_start, data_date_end=data_date_end)

        if not os.path.isdir(GPS_FILE_ROOT):
            os.mkdir(GPS_FILE_ROOT)

        now = datetime.datetime.now()
        time_series = datetime.datetime.strftime(now, '%Y%m%d%H%M%S')
        file_name = 'gps_{time_series}.dbf'.format(time_series=time_series)
        file_path = GPS_FILE_ROOT + file_name
        MakeGPSDbfFile(file_path, sql)
        with open(file_path, "rb") as fprb:
            response = HttpResponse(fprb.read(), content_type='application/x-dbf')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
        os.remove(file_path)
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
            fileJob.create_by = request.user
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


@login_required
def gps_photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            raw_file = form.cleaned_data.get("file")
            fss = FileSystemStorage()
            file = fss.save(raw_file.name, raw_file)
            upload_resut, count = unzip_file("GPS", file, "gps_photo", request.user)

        upload_form = FileUploadForm()
        photo_upload_form = PhotoUploadForm()
        download_form = FileDownloadForm()
        return render(request, 'gps/data_update.html', locals())
