"""
Load content of a DBF file into a Pandas data frame.

The iter() is required because Pandas doesn't detect that the DBF
object is iterable.
"""
from dbfread import DBF
from pandas import DataFrame

table = DBF('_temp.dbf')
for record in table:
    print(record)

#frame = DataFrame(iter(dbf))

#print(frame)