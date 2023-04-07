from django.conf import settings
from django.db import models
from django.utils import timezone


class CarStatus(models.Model):
    status_en = models.CharField(max_length=50)
    status_cn = models.CharField(max_length=50)
    status_desc = models.TextField()
    process_rate = models.IntegerField(default=0)
    create_at = models.DateTimeField(default=timezone.now)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='status_create_at')
    update_at = models.DateTimeField(default=timezone.now)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='status_update_at')

    def __str__(self):
        return self.status_en


class Car(models.Model):
    batch_no = models.CharField(max_length=50)  # 批號
    CARNO = models.CharField(max_length=50, primary_key=True)  # 車號
    CNO = models.CharField(max_length=50)  # 車號數字
    CARTYPE = models.CharField(max_length=50)  # 廠牌型式
    CARCOLOR = models.CharField(max_length=50)  # 顏色
    CARAGE = models.CharField(max_length=50)  # 年份
    COMPANY = models.CharField(max_length=50)  # 單位
    COMPANY2 = models.CharField(max_length=50)  # 記號
    DEBIT = models.CharField(max_length=50)  # 債權
    ENDDATE = models.CharField(max_length=50)  # 動保迄日
    ACCNO = models.CharField(max_length=50)  # 帳號
    GRADE = models.CharField(max_length=50)  # 等級
    COMPMAN = models.CharField(max_length=50)  # 承辦人
    CASENO = models.CharField(max_length=50)  # 案件編號
    CDATE = models.CharField(max_length=50)  # 建檔日期
    FINDMODE = models.CharField(max_length=50)  # 狀態
    CHGDATE = models.CharField(max_length=50)  # 異動日期
    CHGREC = models.CharField(max_length=50)  # 未知
    NOTE2 = models.CharField(max_length=50)  # 備註2
    BNKDATA = models.CharField(max_length=50)  # 未知
    MAN = models.CharField(max_length=50)  # 關聯
    AGE = models.CharField(max_length=50)  # 未知
    CID = models.CharField(max_length=50)  # 證號
    ADDR1 = models.CharField(max_length=255)  # 地址1
    ADDR2 = models.CharField(max_length=255)  # 地址2
    ADDR3 = models.CharField(max_length=255)  # 地址3
    ADDR4 = models.CharField(max_length=255)  # 地址4
    TEL1 = models.CharField(max_length=50)  # 電話1
    TEL2 = models.CharField(max_length=50)  # 電話2
    TEL3 = models.CharField(max_length=50)  # 電話3
    TEL4 = models.CharField(max_length=50)  # 電話4
    OTH1 = models.CharField(max_length=50)  # 主保1
    OTH2 = models.CharField(max_length=50)  # 主保2
    OTH3 = models.CharField(max_length=50)  # 主保3
    OTH4 = models.CharField(max_length=50)  # 主保4
    NEWCHK = models.CharField(max_length=50)  # 未知
    PAUSEDATE = models.CharField(max_length=50)  # 未知
    NOJOIN = models.CharField(max_length=50)  # 未知
    CARNO2 = models.CharField(max_length=50)  # 車號

    def __str__(self):
        return self.CARNO


class CarTemp(models.Model):
    batch_no = models.CharField(max_length=50)  # 批號
    CARNO = models.CharField(max_length=50, primary_key=True)  # 車號
    CNO = models.CharField(max_length=50)  # 車號數字
    CARTYPE = models.CharField(max_length=50)  # 廠牌型式
    CARCOLOR = models.CharField(max_length=50)  # 顏色
    CARAGE = models.CharField(max_length=50)  # 年份
    COMPANY = models.CharField(max_length=50)  # 單位
    COMPANY2 = models.CharField(max_length=50)  # 記號
    DEBIT = models.CharField(max_length=50)  # 債權
    ENDDATE = models.CharField(max_length=50)  # 動保迄日
    ACCNO = models.CharField(max_length=50)  # 帳號
    GRADE = models.CharField(max_length=50)  # 等級
    COMPMAN = models.CharField(max_length=50)  # 承辦人
    CASENO = models.CharField(max_length=50)  # 案件編號
    CDATE = models.CharField(max_length=50)  # 建檔日期
    FINDMODE = models.CharField(max_length=50)  # 狀態
    CHGDATE = models.CharField(max_length=50)  # 異動日期
    CHGREC = models.CharField(max_length=50)  # 未知
    NOTE2 = models.CharField(max_length=50)  # 備註2
    BNKDATA = models.CharField(max_length=50)  # 未知
    MAN = models.CharField(max_length=50)  # 關聯
    AGE = models.CharField(max_length=50)  # 未知
    CID = models.CharField(max_length=50)  # 證號
    ADDR1 = models.CharField(max_length=255)  # 地址1
    ADDR2 = models.CharField(max_length=255)  # 地址2
    ADDR3 = models.CharField(max_length=255)  # 地址3
    ADDR4 = models.CharField(max_length=255)  # 地址4
    TEL1 = models.CharField(max_length=50)  # 電話1
    TEL2 = models.CharField(max_length=50)  # 電話2
    TEL3 = models.CharField(max_length=50)  # 電話3
    TEL4 = models.CharField(max_length=50)  # 電話4
    OTH1 = models.CharField(max_length=50)  # 主保1
    OTH2 = models.CharField(max_length=50)  # 主保2
    OTH3 = models.CharField(max_length=50)  # 主保3
    OTH4 = models.CharField(max_length=50)  # 主保4
    NEWCHK = models.CharField(max_length=50)  # 未知
    PAUSEDATE = models.CharField(max_length=50)  # 未知
    NOJOIN = models.CharField(max_length=50)  # 未知
    CARNO2 = models.CharField(max_length=50)  # 車號

    def __str__(self):
        return self.CARNO
