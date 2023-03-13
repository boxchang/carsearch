from simpledbf import Dbf5

old_path = "car.dbf"
dbfh = Dbf5(old_path, codec='utf-8')
headers = dbfh.fields
hdct = {x[0]: x[1:] for x in headers}