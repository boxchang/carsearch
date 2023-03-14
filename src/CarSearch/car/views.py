from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import os
import uuid
from django.core.paginator import Paginator
from CarSearch.settings.base import MEDIA_ROOT
from car.forms import FileUploadForm
from car.models import Car
from jobs.models import FileJob, JobStatus
import dbfread
from django.urls import reverse

def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)

    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            raw_file = form.cleaned_data.get("file")
            fileJob = FileJob()
            fileJob.file_type = "CAR"
            file_path = handle_uploaded_file(raw_file)
            fileJob.file = file_path
            table = dbfread.DBF(MEDIA_ROOT+file_path)
            fileJob.count = len(table)
            fileJob.status = JobStatus.objects.get(id=1)  # WAIT
            fileJob.create_by = User.objects.get(id=1)
            fileJob.save()
            return redirect(reverse('job_detail'))
    else:
        form = FileUploadForm()

    return render(request, 'car/upload.html', locals())


def search(request):
    if request.method == 'POST':
        page_number = 1
        #cars = Car.objects.all()
        sql = """SELECT * FROM car_car where 1=1 """
        car_status = request.POST.get('car_status')
        keyword = request.POST.get('keyword')

        if keyword:
            sql += """ and (CARNO like '%%{keyword}%%' or ADDR1 like '%%{keyword}%%')""".format(keyword=keyword)


        if car_status:
            sql += """and FINDMODE='{status}'""".format(status=car_status)
            if car_status == "待  尋":
                car_status_find = "selected"
            elif car_status == "取  消":
                car_status_cancel = "selected"
            else:
                car_status_all = "selected"

        cars = Car.objects.raw(sql)

        results = list(cars)
        page_obj = Paginator(results, 50)
        row_count = len(results)

        if page_number:
            page_results = page_obj.page(page_number)
        else:
            page_results = page_obj.page(1)

        return render(request, 'car/search.html', locals())

    return render(request, 'car/search.html', locals())


def detail(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            raw_file = form.cleaned_data.get("file")
            fileJob = FileJob()
            fileJob.file_type = "CAR"
            file_path = handle_uploaded_file(raw_file)
            fileJob.file = file_path
            table = dbfread.DBF(MEDIA_ROOT+file_path)
            fileJob.count = len(table)
            fileJob.status = JobStatus.objects.get(id=1)  # WAIT
            fileJob.create_by = User.objects.get(id=1)
            fileJob.save()
            return redirect(reverse('car_detail'))
    else:
        form = FileUploadForm()

    return render(request, 'car/upload.html', locals())