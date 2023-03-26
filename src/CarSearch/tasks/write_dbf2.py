import datetime

import dbf

from bases.database import database
from bases.utils import Cursor2Dict



new_table = dbf.Table('gps_temp.dbf', 'CARNO_2 C(8); NO_2 C(4); DATE_2 D; TIME_2 C(5); ADDR_2 C(30); GPS_2A N(10,4); '
                                      'GPS_2B N(10,4); MARK_2 L; SALES_2 C(12); BINGO_2 D; UPDATE_2 D', codepage='cp950')

new_table.open(dbf.READ_WRITE)


db = database()
conn = db.create_connection()
sql = "select * from gps_gps"
rows = Cursor2Dict(conn, sql)
i = 0
for row in rows:
    if i==322:
        print("xxx")
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
