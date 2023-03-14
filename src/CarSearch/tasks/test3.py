
import dbfread

from bases.database import database

db = database()
def execute_sql(sql):
    db.execute_sql(sql)


table = dbfread.DBF('car2.dbf', load=True, char_decode_errors='ignore')


i = 1

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
    if i % 3000 == 0:
        execute_sql(values_sql[:-1])
        values_sql = "INSERT INTO car_car {colums} VALUES ".format(colums=fields_sql)  # 初始化

    values_str = ','.join("'{value}'".format(value=str(record[field]).replace("'", "''")) for field in fields)
    values_sql += "('batch_no',{value}),".format(value=values_str)
    i += 1
    print(i)

execute_sql(values_sql[:-1])

print(i)

#records = table.sql("select * where CARNO = '3C-6149'")