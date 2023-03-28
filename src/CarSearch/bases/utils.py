import dbfread
import MySQLdb
import os
import uuid
from datetime import datetime
from bases.database import database


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
        now = datetime.now()
        self.start_time = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        db = database()
        sql = """update jobs_filejob set status_id = '{status_id}', success={count}, start_time='{start_time}' where batch_no = '{batch_no}'""".format(
            status_id=status_id, count=count, batch_no=batch_no, start_time=self.start_time
        )
        db.execute_sql(sql)



    def filejob_end_update(self, batch_no, status_id, count):
        now = datetime.now()
        start_time = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')
        exe_time = now - start_time
        end_time = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
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
