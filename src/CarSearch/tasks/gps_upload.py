import dbfread
from datetime import datetime
from CarSearch.settings.base import MEDIA_ROOT
from bases.database import database
from bases.utils import Cursor2Dict, FileUploadJob


class GPS_Upload(object):
    start_time = ""
    end_time = ""
    conn = ""

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
        count = 0
        for record in table:
            if self.chkRecord(record):
                try:
                    self.insertRecord(batch_no, record)
                    count += 1
                except:
                    pass
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


    def execute(self):
        upload = FileUploadJob()

        sql = """select * from jobs_filejob where status_id='1' and file_type='GPS'"""
        rows = Cursor2Dict(self.conn, sql)
        for row in rows:
            file_name = row['file']
            batch_no = row['batch_no']
            file_path = MEDIA_ROOT + file_name
            upload.filejob_start_update(batch_no, '2', 0)  # ON-Going
            count = self.insertDbfFile(batch_no, file_path)
            upload.filejob_end_update(batch_no, '3', count)  # DONE


# obj = GPS_Upload()
# obj.execute()
