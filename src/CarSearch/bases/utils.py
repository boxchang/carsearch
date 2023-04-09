import zipfile

import dbfread
import MySQLdb
import os
import uuid
import datetime

from CarSearch.settings.base import MEDIA_ROOT
from bases.database import database
import dbf

from car.models import CAR_PHOTO
from gps.models import GPS_PHOTO
from users.models import UploadRecord


class JOB_STATUS(object):
    WAIT = 1
    ON_GOING = 2
    DONE = 3


class FileUploadJob(object):
    start_time = ""

    def handle_uploaded_file(self, file):
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


    def filejob_start_update(self, batch_no, status_id, count):
        now = datetime.datetime.now()
        self.start_time = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        db = database()
        sql = """update jobs_filejob set status_id = '{status_id}', success={count}, start_time='{start_time}' where batch_no = '{batch_no}'""".format(
            status_id=status_id, count=count, batch_no=batch_no, start_time=self.start_time
        )
        db.execute_sql(sql)



    def filejob_end_update(self, batch_no, status_id, count):
        now = datetime.datetime.now()
        start_time = datetime.datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
        exe_time = now - start_time
        end_time = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        db = database()
        sql = """update jobs_filejob set status_id = '{status_id}', success={count}, end_time='{end_time}', exe_time={exe_time} where batch_no = '{batch_no}'""".format(
            status_id=status_id, count=count, batch_no=batch_no, end_time=end_time, exe_time=exe_time.seconds
        )
        db.execute_sql(sql)


'''
讀取DBF文件
'''
def readDbfFile(self, filename):
    table = dbfread.DBF(filename)
    self.open_conn()
    self.cur = self.conn.cursor()
    for field in table.fields:
        print(field)


def Cursor2Dict(conn, sql):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    return cur.fetchall()


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def MakeGPSDbfFile(file_name, sql):
    new_table = dbf.Table(file_name,
                          'CARNO_2 C(8); NO_2 C(4); DATE_2 D; TIME_2 C(5); ADDR_2 C(30); GPS_2A N(10,4); '
                          'GPS_2B N(10,4); MARK_2 L; SALES_2 C(12); BINGO_2 D; UPDATE_2 D', codepage='cp950')

    new_table.open(dbf.READ_WRITE)

    db = database()
    conn = db.create_connection()
    rows = Cursor2Dict(conn, sql)
    i = 0
    for row in rows:
        # 資料整理
        if row['BINGO_2'] == 'None':
            row['BINGO_2'] = None
        else:
            row['BINGO_2'] = datetime.datetime.strptime(row['BINGO_2'], '%Y-%m-%d')

        if row['UPDATE_2'] == 'None':
            row['UPDATE_2'] = None
        else:
            row['UPDATE_2'] = datetime.datetime.strptime(row['UPDATE_2'], '%Y-%m-%d')

        # 轉成Tuple
        row_tuple = (row['CARNO_2'], row['NO_2'],
                          datetime.datetime.strptime(row['DATE_2'], '%Y-%m-%d'),
                          row['TIME_2'], row['ADDR_2'], row['GPS_2A'],
                          row['GPS_2B'], bool(row['MARK_2']),
                          row['SALES_2'], row['BINGO_2'], row['UPDATE_2'])

        new_table.append(row_tuple)
        i += 1
    new_table.close()


def MakeCarDbfFile(file_name, sql):
    new_table = dbf.Table(file_name,
                          'CARNO C(8); NO C(4); CARTYPE C(12); CARCOLOR C(4); CARAGE C(4); COMPANY C(40); '
                          'COMPANY2 C(4); DEBIT C(8); ENDDATE C(9); ACCNO C(15); GRADE C(4); COMPMAN C(10); '
                          'CASENO C(15); DATE D; FINDMODE C(6); CHGDATE D; CHGREC C(65); NOTE2 C(50); BNKDATA L; '
                          'MAN C(10); AGE N(3,0); ID C(10); ADDR1 C(50); ADDR2 C(50); ADDR3 C(50); ADDR4 C(50); '
                          'TEL1 C(15); TEL2 C(15); TEL3 C(15); TEL4 C(15); OTH1 C(8); OTH2 C(8); OTH3 C(8); OTH4 C(8); '
                          'NEWCHK L; PAUSEDATE D; NOJOIN L;', codepage='cp950')

    new_table.open(dbf.READ_WRITE)

    db = database()
    conn = db.create_connection()
    rows = Cursor2Dict(conn, sql)
    count = 0
    for row in rows:
        # 資料整理
        if row['CDATE'] == 'None':
            row['CDATE'] = None
        else:
            row['CDATE'] = datetime.datetime.strptime(row['CDATE'], '%Y-%m-%d')

        if row['CHGDATE'] == 'None':
            row['CHGDATE'] = None
        else:
            row['CHGDATE'] = datetime.datetime.strptime(row['CHGDATE'], '%Y-%m-%d')

        if row['PAUSEDATE'] == 'None':
            row['PAUSEDATE'] = None
        else:
            row['PAUSEDATE'] = datetime.datetime.strptime(row['PAUSEDATE'], '%Y-%m-%d')

        # 轉成Tuple
        row_tuple = (row['CARNO'], row['CNO'],row['CARTYPE'], row['CARCOLOR'],row['CARAGE'],
                     row['COMPANY'], row['COMPANY2'], row['DEBIT'], row['ENDDATE'], row['ACCNO'],
                     row['GRADE'], row['COMPMAN'], row['CASENO'], row['CDATE'],row['FINDMODE'],
                     row['CHGDATE'],row['CHGREC'], row['NOTE2'], bool(row['BNKDATA']), row['MAN'], row['AGE'],
                     row['CID'], row['ADDR1'], row['ADDR2'], row['ADDR3'], row['ADDR4'], row['TEL1'],
                     row['TEL2'], row['TEL3'], row['TEL4'], row['OTH1'], row['OTH2'], row['OTH3'],
                     row['OTH4'], bool(row['NEWCHK']), row['PAUSEDATE'], bool(row['NOJOIN']))

        new_table.append(row_tuple)
        count += 1
    new_table.close()
    return count

def unzip_file(type, file, unzip_path, user):
    try:
        # 查看 ZIP 壓縮檔內容資訊
        file_path = MEDIA_ROOT + file
        count = 0
        batch_no = uuid.uuid4().hex[:10]



        with zipfile.ZipFile(file_path, 'r') as zf:
            # 透過 InfoInfo 物件查看 ZIP 檔案內容
            # 解壓縮前先紀錄Record
            for info in zf.infolist():
                if info.filename[-4:] == ".jpg" or info.filename[-4:] == ".png":
                    count += 1
                    print(info)
                    if type == "CAR":
                        if str(info.filename).find("_") > 0:
                            raise Exception("檔案格式不符")
                        photo = CAR_PHOTO()
                        photo.CARNO = info.filename[:str(info.filename).find(".")]
                        photo.FILE = info.filename
                        photo.save()
                    elif type == "GPS":
                        photo = GPS_PHOTO()
                        gps_info = info.filename.split("_")
                        photo.FILE = info.filename[str(info.filename).find("/")+1:]
                        photo.CARNO = gps_info[0][str(gps_info[0]).find("/")+1:]
                        photo.DATE = gps_info[1]
                        photo.TIME = gps_info[2]
                        photo.GPS_2A = gps_info[3]
                        photo.GPS_2B = gps_info[4]
                        photo.save()

            record = UploadRecord()
            record.type = type
            record.batch_no = batch_no
            record.user = user
            record.count = count
            record.save()

            absolute_file_path = MEDIA_ROOT + unzip_path
            directory = os.path.dirname(absolute_file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # 解壓縮所有檔案至 car_photo 目錄
            zf.extractall(path=absolute_file_path)
        os.remove(file_path)
        upload_resut = "success"
    except Exception as e:
        print(e)
        upload_resut = "fail"
    return upload_resut, count




