from dbfread import DBF

for record in DBF('car2.dbf', load=True, char_decode_errors='ignore'):
    if record['CARNO'] == "NNS-0786":
        pass