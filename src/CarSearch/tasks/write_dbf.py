from dbfpy import dbf

'''
寫DBF文件
@filename 文件名
@header   列頭
@content  內容
'''
def writeDbfFile(filename, header, content):
    # 打開dbf
    db = dbf.Dbf(filename, new=True)
    # 寫列頭
    for field in header:
        # 此處需要改成長度可配的，長度太短會導致數據被截斷
        if type(field) == unicode:
            field = field.encode('GBK')
        db.addField((field, 'C', 20))

    # 寫數據
    for record in content:
        rec = db.newRecord()
        for key, value in itertools.izip(header, record):
            if type(value) == unicode:
                rec[key] = value.encode('GBK')
            else:
                rec[key] = value
            rec.store()
    # 關閉文檔
    db.close()