import MySQLdb
from django.shortcuts import render
import dbfread

'''
讀取DBF文件
'''
def readDbfFile(self, filename):
    table = dbfread.DBF(filename)
    self.open_conn()
    self.cur = self.conn.cursor()
    for field in table.fields:
        print(field)

def Cursor2Dict(conn, sql):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    return cur.fetchall()


def index(request):
    return render(request, 'bases/info.html', locals())


def history(request):
    return render(request, 'bases/history.html', locals())
