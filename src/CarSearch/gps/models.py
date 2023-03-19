from django.db import models
from django.conf import settings
from django.utils import timezone


class GPS(models.Model):
    batch_no = models.CharField(max_length=50)
    CARNO_2 = models.CharField(max_length=50)
    NO_2 = models.CharField(max_length=50)
    DATE_2 = models.CharField(max_length=50)
    TIME_2 = models.CharField(max_length=50)
    ADDR_2 = models.CharField(max_length=50)
    GPS_2A = models.CharField(max_length=50)
    GPS_2B = models.CharField(max_length=50)
    MARK_2 = models.CharField(max_length=50)
    SALES_2 = models.CharField(max_length=50)
    BINGO_2 = models.CharField(max_length=50)
    UPDATE_2 = models.CharField(max_length=50)


    class Meta:
        unique_together = ('CARNO_2', 'DATE_2', 'TIME_2')


    def __str__(self):
        return self.CARNO_2