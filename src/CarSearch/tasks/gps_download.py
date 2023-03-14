from bases.database import database


class CarSearch(object):
    start_time = ""
    end_time = ""

    def __init__(self):
        db = database()
        self.conn = db.create_connection()


    def execute(self):
        sql = """select * from jobs_filejob where file_type='GPS'"""
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)



obj = CarSearch()
obj.execute()