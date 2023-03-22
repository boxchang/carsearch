# Generated by Django 2.2 on 2023-03-22 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20230319_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='create_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_create_dt', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='update_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_update_dt', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='expired_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='帳號到期日'),
        ),
        migrations.CreateModel(
            name='UserAuthority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CARTYPE', models.BooleanField(default=False)),
                ('CARCOLOR', models.BooleanField(default=False)),
                ('CARAGE', models.BooleanField(default=False)),
                ('COMPANY', models.BooleanField(default=False)),
                ('COMPANY2', models.BooleanField(default=False)),
                ('DEBIT', models.BooleanField(default=False)),
                ('ENDDATE', models.BooleanField(default=False)),
                ('ACCNO', models.BooleanField(default=False)),
                ('GRADE', models.BooleanField(default=False)),
                ('COMPMAN', models.BooleanField(default=False)),
                ('CASENO', models.BooleanField(default=False)),
                ('VDATE', models.BooleanField(default=False)),
                ('FINDMODE', models.BooleanField(default=False)),
                ('CHGDATE', models.BooleanField(default=False)),
                ('CHGREC', models.BooleanField(default=False)),
                ('NOTE2', models.BooleanField(default=False)),
                ('MAN', models.BooleanField(default=False)),
                ('VID', models.BooleanField(default=False)),
                ('ADDR1', models.BooleanField(default=False)),
                ('ADDR2', models.BooleanField(default=False)),
                ('ADDR3', models.BooleanField(default=False)),
                ('ADDR4', models.BooleanField(default=False)),
                ('TEL1', models.BooleanField(default=False)),
                ('TEL2', models.BooleanField(default=False)),
                ('TEL3', models.BooleanField(default=False)),
                ('TEL4', models.BooleanField(default=False)),
                ('OTH1', models.BooleanField(default=False)),
                ('OTH2', models.BooleanField(default=False)),
                ('OTH3', models.BooleanField(default=False)),
                ('OTH4', models.BooleanField(default=False)),
                ('DOWNLOAD_CAR_LIST', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_authority', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]