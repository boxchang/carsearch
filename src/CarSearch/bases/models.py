from django.db import models


class EmailSetting(models.Model):
    server = models.CharField(max_length=50)
    port = models.IntegerField()
    account = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mail_from = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    mail_body = models.CharField(max_length=1000)
