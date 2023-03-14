import dbfread
from datetime import datetime
from CarSearch.settings.base import MEDIA_ROOT
from bases.database import database
from bases.utils import Cursor2Dict, FileUploadJob


class CAR_Upload(object):
    start_time = ""
    end_time = ""

    def log(self, msg):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("{CurrentTime} {msg}".format(CurrentTime=current_time, msg=msg))

    '''
    新增DBF資料
    '''
    def insertDbfFile(self, batch_no, filename):
        db = database()
        table = dbfread.DBF(filename, load=True, char_decode_errors='ignore')

        count = 1

        fields = table.field_names
        db_fields = []
        for field in fields:
            if field == "NO":
                field = "CNO"

            if field == "ID":
                field = "CID"

            if field == "DATE":
                field = "CDATE"

            db_fields.append(field)

        fields_str = ','.join(db_fields)
        fields_sql = "(batch_no, {colums})".format(colums=fields_str)

        values_sql = "INSERT INTO car_car {colums} VALUES ".format(colums=fields_sql)
        for record in table:
            if count % 3000 == 0:
                db.execute_sql(values_sql[:-1])
                values_sql = "INSERT INTO car_car {colums} VALUES ".format(colums=fields_sql)  # 初始化

            values_str = ','.join("'{value}'".format(value=str(record[field]).replace("'", "''")) for field in fields)
            values_sql += "('{batch_no}',{value}),".format(batch_no=batch_no, value=values_str)
            count += 1

        db.execute_sql(values_sql[:-1])

        return count


    def execute(self):
        upload = FileUploadJob()
        db = database()
        conn = db.create_connection()
        sql = """select * from jobs_filejob where status_id='1' and file_type='CAR'"""
        rows = Cursor2Dict(conn, sql)
        for row in rows:
            file_name = row['file']
            batch_no = row['batch_no']
            file_path = MEDIA_ROOT + file_name
            upload.filejob_start_update(batch_no, '2', 0)  # ON-Going
            count = self.insertDbfFile(batch_no, file_path)
            upload.filejob_end_update(batch_no, '3', count)  # DONE

    def delete_car_data(self):
        db = database()
        sql = "delete from car_car"
        db.execute_sql(sql)




obj = CAR_Upload()
obj.delete_car_data()
obj.execute()