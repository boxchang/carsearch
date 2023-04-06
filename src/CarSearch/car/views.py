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
from users.models import CustomUser, SearchRecord


@login_required
class SearchCondition(object):
    car_status = ""
    keyword = ""
    carcolor = ""
    carage = ""
    enddate_start = ""
    enddate_end = ""
    chgdate_start = ""
    chgdate_end = ""
    car_status_find = ""
    car_status_cancel = ""

    def __init__(self, request):
        if request.method == 'POST':
            self.init_session(request)
            self.car_status = request.POST.get('car_status')
            self.keyword = request.POST.get('keyword')
            self.addr = request.POST.get('addr')
            self.carcolor = request.POST.get('carcolor')
            self.carage = request.POST.get('carage')
            self.enddate_start = request.POST.get('enddate_start')
            self.enddate_end = request.POST.get('enddate_end')
            self.chgdate_start = request.POST.get('chgdate_start')
            self.chgdate_end = request.POST.get('chgdate_end')

            if self.keyword:
                request.session['keyword'] = self.keyword

            if self.car_status == "待  尋":
                request.session['car_status_find'] = "selected"
            elif self.car_status == "取  消":
                request.session['car_status_cancel'] = "selected"
            else:
                request.session['car_status_all'] = "selected"

            if self.carcolor:
                request.session['carcolor'] = self.carcolor

            if self.carage:
                request.session['carage'] = self.carage

            if self.enddate_start:
                request.session['enddate_start'] = self.enddate_start

            if self.enddate_end:
                request.session['enddate_end'] = self.enddate_end

            if self.chgdate_start:
                request.session['chgdate_start'] = self.chgdate_start

            if self.chgdate_end:
                request.session['chgdate_end'] = self.chgdate_end

        if request.method == "GET":
            if 'keyword' in request.session:
                self.keyword = request.session['keyword']

            if 'car_status_find' in request.session:
                self.car_status_find = "待  尋"

            if 'car_status_cancel' in request.session:
                self.car_status_cancel = "取  消"

            if 'carcolor' in request.session:
                self.carcolor = request.session['carcolor']

            if 'carage' in request.session:
                self.carage = request.session['carage']

            if 'enddate_start' in request.session:
                self.enddate_start = request.session['enddate_start']

            if 'enddate_end' in request.session:
                self.enddate_end = request.session['enddate_end']

            if 'chgdate_start' in request.session:
                self.chgdate_start = request.session['chgdate_start']

            if 'chgdate_end' in request.session:
                self.chgdate_end = request.session['chgdate_end']

    def init_session(self, request):
        if 'keyword' in request.session:
            del request.session['keyword']

        if 'car_status_find' in request.session:
            del request.session['car_status_find']

        if 'car_status_cancel' in request.session:
            del request.session['car_status_cancel']

        if 'carcolor' in request.session:
            del request.session['carcolor']

        if 'carage' in request.session:
            del request.session['carage']

        if 'enddate_start' in request.session:
            del request.session['enddate_start']

        if 'enddate_end' in request.session:
            del request.session['enddate_end']

        if 'chgdate_start' in request.session:
            del request.session['chgdate_start']

        if 'chgdate_end' in request.session:
            del request.session['chgdate_end']


@login_required
def car_data_update(request):
    upload_form = FileUploadForm()

    return render(request, 'car/data_update.html', locals())


@login_required
def download(request):
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
            table = dbfread.DBF(MEDIA_ROOT + file_path)
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
            table = dbfread.DBF(MEDIA_ROOT + file_path)
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

    return render(request, 'car/data_update.html', locals())


@login_required
def search(request):
    page_number = 1
    keyword = ""
    car_status = ""
    log_words = ""
    condition = SearchCondition(request)

    if request.method == "GET":
        page_number = request.GET.get('page')

    sql = """SELECT * FROM car_car where 1=1 """
    if condition.keyword:
        log_words += "車牌或地址：{keyword};".format(keyword=condition.keyword)
        sql += """ and (CARNO like '%%{keyword}%%' 
        or ADDR1 like '%%{keyword}%%' 
        or ADDR2 like '%%{keyword}%%' 
        or ADDR3 like '%%{keyword}%%' 
        or ADDR4 like '%%{keyword}%%' 
        or CARNO2 like '%%{keyword}%%')""".format(keyword=condition.keyword)

    if condition.car_status:
        log_words += "狀態：{car_status};".format(car_status=condition.car_status)
        sql += """and FINDMODE='{status}'""".format(status=condition.car_status)

    if condition.carcolor:
        log_words += "顏色：{carcolor};".format(carcolor=condition.carcolor)
        sql += """and CARCOLOR='{color}'""".format(color=condition.carcolor)

    if condition.carage:
        log_words += "年份：{carage};".format(carage=condition.carage)
        sql += """and CARAGE='{age}'""".format(age=condition.carage)

    if condition.enddate_start and condition.enddate_end:
        log_words += "動保迄日：{enddate_start}~{enddate_end};".format(enddate_start=condition.enddate_start, enddate_end=condition.enddate_end)
        sql += """and ENDDATE between '{end_date_start}' and '{end_date_end}'"""\
            .format(end_date_start=condition.enddate_start, end_date_end=condition.enddate_end)

    if condition.chgdate_start and condition.chgdate_end:
        log_words += "異動日期：{chgdate_start}~{chgdate_end};".format(chgdate_start=condition.chgdate_start, chgdate_end=condition.chgdate_end)
        sql += """and CHGDATE between '{chg_date_start}' and '{chg_date_end}'"""\
            .format(chg_date_start=condition.chgdate_start, chg_date_end=condition.chgdate_end)

    cars = Car.objects.raw(sql)
    results = list(cars)
    page_obj = Paginator(results, 50)
    row_count = len(results)

    # Log
    record = SearchRecord()
    record.user = request.user
    record.words = log_words
    record.match_count = row_count
    record.save()

    # 分頁
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
    for gps in gpss:
        gps.GPS_2A = (float(gps.GPS_2A[3:])/60)+float(gps.GPS_2A[0:3])  # 經度 22
        gps.GPS_2B = (float(gps.GPS_2B[2:])/60)+float(gps.GPS_2B[0:2])  # 緯度 120

    return render(request, 'car/detail.html', locals())


def run_upload():
    obj = CAR_Upload()
    obj.delete_car_data()
    obj.execute()
