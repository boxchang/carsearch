from django.http import HttpResponse
from django.shortcuts import render, redirect
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
import datetime
import dbf
from bases.database import database
from bases.utils import Cursor2Dict
import os


@login_required
def gps_data_update(request):
    upload_form = FileUploadForm()
    download_form = FileDownloadForm()
    return render(request, 'gps/data_update.html', locals())


@login_required
def gps_data_download(request):
    file_name = GPS_FILE_ROOT+'gps_temp.dbf'
    new_table = dbf.Table(file_name,
                          'CARNO_2 C(8); NO_2 C(4); DATE_2 D; TIME_2 C(5); ADDR_2 C(30); GPS_2A N(10,4); '
                          'GPS_2B N(10,4); MARK_2 L; SALES_2 C(12); BINGO_2 D; UPDATE_2 D', codepage='cp950')

    new_table.open(dbf.READ_WRITE)

    db = database()
    conn = db.create_connection()
    sql = "select * from gps_gps"
    rows = Cursor2Dict(conn, sql)
    i = 0
    for row in rows:
        if row['BINGO_2'] == 'None':
            row['BINGO_2'] = None
        else:
            row['BINGO_2'] = datetime.datetime.strptime(row['BINGO_2'], '%Y-%m-%d')

        if row['UPDATE_2'] == 'None':
            row['UPDATE_2'] = None
        else:
            row['UPDATE_2'] = datetime.datetime.strptime(row['UPDATE_2'], '%Y-%m-%d')

        new_table.append({'CARNO_2': row['CARNO_2'], 'NO_2': row['NO_2'],
                          'DATE_2': datetime.datetime.strptime(row['DATE_2'], '%Y-%m-%d'),
                          'TIME_2': row['TIME_2'], 'ADDR_2': row['ADDR_2'], 'GPS_2A': row['GPS_2A'],
                          'GPS_2B': row['GPS_2B'], 'MARK_2': bool(row['MARK_2']),
                          'SALES_2': row['SALES_2'], 'BINGO_2': row['BINGO_2'], 'UPDATE_2': row['UPDATE_2']})
        i += 1
    new_table.close()

    with open(file_name, "rb") as fprb:
        response = HttpResponse(fprb.read(), content_type='application/x-dbf')
        response['Content-Disposition'] = 'attachment; filename='+file_name
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