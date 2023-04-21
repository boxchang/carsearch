from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

from bases.forms import SettingForm
from car.models import Car

@login_required
def setting(request):
    form = SettingForm()
    return render(request, 'bases/setting.html', locals())


@login_required
def index(request):
    cursor = connection.cursor()
    sql = """SELECT a.CARNO, a.CARTYPE, a.CARCOLOR, a.FINDMODE, a.ADDR1 
            FROM car_car a LEFT OUTER JOIN car_car2 b ON a.CARNO = b.CARNO WHERE (b.CARNO IS NULL OR a.FINDMODE <> b.FINDMODE)"""
    cars = Car.objects.raw(sql)
    row_count = format(len(list(cars)), ',')


    sql = "SELECT COUNT(*) FROM car_car WHERE FINDMODE='待  尋'"
    cursor.execute(sql)
    find_count = format(cursor.fetchone()[0], ',')


    sql = """SELECT COUNT(*) FROM car_car"""
    cursor.execute(sql)
    all_count = format(cursor.fetchone()[0], ',')


    sql = """SELECT MAX(end_time) update_time FROM jobs_filejob a WHERE a.file_type = 'CAR'"""
    cursor.execute(sql)
    update_time = cursor.fetchone()[0]


    return render(request, 'bases/info.html', locals())


@login_required
def history(request):
    return render(request, 'bases/history.html', locals())

