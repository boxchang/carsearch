# Generated by Django 2.2 on 2023-03-09 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CARNO', models.CharField(max_length=50)),
                ('CNO', models.CharField(max_length=50)),
                ('CARTYPE', models.CharField(max_length=50)),
                ('CARCOLOR', models.CharField(max_length=50)),
                ('CARAGE', models.CharField(max_length=50)),
                ('COMPANY', models.CharField(max_length=50)),
                ('COMPANY2', models.CharField(max_length=50)),
                ('DEBIT', models.CharField(max_length=50)),
                ('ENDDATE', models.CharField(max_length=50)),
                ('ACCNO', models.CharField(max_length=50)),
                ('GRADE', models.CharField(max_length=50)),
                ('COMPMAN', models.CharField(max_length=50)),
                ('CASENO', models.CharField(max_length=50)),
                ('CDATE', models.CharField(max_length=50)),
                ('FINDMODE', models.CharField(max_length=50)),
                ('CHGDATE', models.CharField(max_length=50)),
                ('CHGREC', models.CharField(max_length=50)),
                ('NOTE2', models.CharField(max_length=50)),
                ('BNKDATA', models.CharField(max_length=50)),
                ('MAN', models.CharField(max_length=50)),
                ('AGE', models.CharField(max_length=50)),
                ('CID', models.CharField(max_length=50)),
                ('ADDR1', models.CharField(max_length=255)),
                ('ADDR2', models.CharField(max_length=255)),
                ('ADDR3', models.CharField(max_length=255)),
                ('ADDR4', models.CharField(max_length=255)),
                ('TEL1', models.CharField(max_length=50)),
                ('TEL2', models.CharField(max_length=50)),
                ('TEL3', models.CharField(max_length=50)),
                ('TEL4', models.CharField(max_length=50)),
                ('OTH1', models.CharField(max_length=50)),
                ('OTH2', models.CharField(max_length=50)),
                ('OTH3', models.CharField(max_length=50)),
                ('OTH4', models.CharField(max_length=50)),
                ('NEWCHK', models.CharField(max_length=50)),
                ('PAUSEDATE', models.CharField(max_length=50)),
                ('NOJOIN', models.CharField(max_length=50)),
            ],
        ),
    ]
