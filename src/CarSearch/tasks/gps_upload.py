import dbfread
from datetime import datetime

from CarSearch.settings.base import MEDIA_ROOT
from bases.database import database
from bases.views import Cursor2Dict



class CarSearch(object):
    start_time = ""
    end_time = ""

    def __init__(self):
        db = database()
        self.conn = db.create_connection()

    def log(self, msg):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("{CurrentTime} {msg}".format(CurrentTime=current_time, msg=msg))

    '''
    新增DBF資料
    '''
    def insertDbfFile(self, batch_no, filename):
        table = dbfread.DBF(filename)
        self.log("Start Insert")
        print(len(table))
        count = 1
        for record in table:
            if self.chkRecord(record):
                self.insertRecord(batch_no, record)
                count += 1
        print("共{count}筆".format(count=count))
        self.log("End Insert")
        return count

    def chkRecord(self, record):
        bResult = False
        sql = """select * from gps_gps where CARNO_2='{CARNO_2}' and DATE_2='{DATE_2}' and TIME_2='{TIME_2}'""".format(
            CARNO_2=record['CARNO_2'],
            DATE_2=record['DATE_2'],
            TIME_2=record['TIME_2']
        )
        cur = self.conn.cursor()
        cur.execute(sql)
        if cur.rowcount == 0:
            bResult = True
        return bResult

    def insertRecord(self, batch_no, record):
        db = database()
        sql = """insert into gps_gps(batch_no,carno_2,no_2,date_2,time_2,addr_2,gps_2a,gps_2b,
                            mark_2,sales_2,bingo_2,update_2)
                Values('{batch_no}','{CARNO_2}','{NO_2}','{DATE_2}','{TIME_2}','{ADDR_2}','{GPS_2A}','{GPS_2B}',
                        '{MARK_2}','{SALES_2}','{BINGO_2}','{UPDATE_2}')""".format(
            batch_no=batch_no,
            CARNO_2=record['CARNO_2'],
            NO_2=record['NO_2'],
            DATE_2=record['DATE_2'],
            TIME_2=record['TIME_2'],
            ADDR_2=record['ADDR_2'],
            GPS_2A=record['GPS_2A'],
            GPS_2B=record['GPS_2B'],
            MARK_2=record['MARK_2'],
            SALES_2=record['SALES_2'],
            BINGO_2=record['BINGO_2'],
            UPDATE_2=record['UPDATE_2'])
        db.execute_sql(sql)

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
        self.end_time = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
        db = database()
        sql = """update jobs_filejob set status_id = '{status_id}', success={count}, end_time='{end_time}', exe_time={exe_time} where batch_no = '{batch_no}'""".format(
            status_id=status_id, count=count, batch_no=batch_no, end_time=self.end_time, exe_time=exe_time.seconds
        )
        db.execute_sql(sql)


    def execute(self):
        sql = """select * from jobs_filejob where status_id='1' and file_type='GPS'"""
        rows = Cursor2Dict(self.conn, sql)
        for row in rows:
            file_name = row['file']
            batch_no = row['batch_no']
            self.filejob_start_update(batch_no, '2', 0)  # ON-Going
            file_path = MEDIA_ROOT + file_name
            count = self.insertDbfFile(batch_no, file_path)
            self.filejob_end_update(batch_no, '3', count)  # DONE


obj = CarSearch()
obj.execute()