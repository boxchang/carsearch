from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from CarSearch.settings.base import MEDIA_ROOT
from bases.utils import FileUploadJob
from car.forms import FileUploadForm
from car.models import Car
from gps.models import GPS
from jobs.models import FileJob, JobStatus
import dbfread
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import threading

from tasks.car_upload import CAR_Upload
from users.models import CustomUser


@login_required
def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            raw_file = form.cleaned_data.get("file")
            fileJob = FileJob()
            fileJob.file_type = "CAR"
            batch_no, file_path = FileUploadJob().handle_uploaded_file(raw_file)
            fileJob.batch_no = batch_no
            fileJob.file = file_path
            table = dbfread.DBF(MEDIA_ROOT+file_path)
            fileJob.count = len(table)
            fileJob.status = JobStatus.objects.get(id=1)  # WAIT
            fileJob.create_by = CustomUser.objects.get(id=1)
            fileJob.save()

            t = threading.Thread(target=run_upload)
            t.setDaemon(True)  # 主線程不管子線程的結果
            t.start()

            return redirect(reverse('job_detail'))
    else:
        form = FileUploadForm()

    return render(request, 'car/upload.html', locals())


def search(request):
    page_number = 1
    keyword = ""
    car_status = ""
    sql = """SELECT * FROM car_car where 1=1 """
    if request.method == 'POST':

        car_status = request.POST.get('car_status')
        keyword = request.POST.get('keyword')

    if request.method == "GET":
        page_number = request.GET.get('page')
        if 'car_status' in request.session:
            car_status = request.session['car_status']

        if 'keyword' in request.session:
            keyword = request.session['keyword']

        if 'car_status_find' in request.session:
            car_status = "待  尋"

        if 'car_status_cancel' in request.session:
            car_status = "取  消"

    if keyword:
        sql += """ and (CARNO like '%%{keyword}%%' or ADDR1 like '%%{keyword}%%')""".format(keyword=keyword)
        request.session['keyword'] = keyword
    else:
        if 'keyword' in request.session:
            del request.session['keyword']

    if car_status:
        sql += """and FINDMODE='{status}'""".format(status=car_status)
    else:
        if 'car_status_find' in request.session:
            del request.session['car_status_find']

        if 'car_status_cancel' in request.session:
            del request.session['car_status_cancel']

    if car_status == "待  尋":
        request.session['car_status_find'] = "selected"
    elif car_status == "取  消":
        request.session['car_status_cancel'] = "selected"
    else:
        request.session['car_status_all'] = "selected"

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


def detail(request, pk):
    car = Car.objects.get(pk=pk)
    if car.FINDMODE == "待  尋":
        color = "b02a37"
    elif car.FINDMODE == "取  消":
        color = "FF0000"
    else:
        color = "000000"

    gpss = GPS.objects.filter(CARNO_2=pk).order_by('-DATE_2', '-TIME_2')

    return render(request, 'car/detail.html', locals())


def run_upload():
    obj = CAR_Upload()
    obj.delete_car_data()
    obj.execute()
