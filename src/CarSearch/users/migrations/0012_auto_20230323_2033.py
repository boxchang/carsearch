# Generated by Django 2.2 on 2023-03-23 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20230323_1957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('view_cartype', 'view_cartype'), ('view_carcolor', 'view_carcolor'), ('view_carage', 'view_carage'), ('view_company', 'view_company'), ('view_company2', 'view_company2'), ('view_debit', 'view_debit'), ('view_enddate', 'view_enddate'), ('view_accno', 'view_accno'), ('view_grade', 'view_grade'), ('view_compman', 'view_compman'), ('view_caseno', 'view_caseno'), ('view_cdate', 'view_cdate'), ('view_findmode', 'view_findmode'), ('view_chgdate', 'view_chgdate'), ('view_chgrec', 'view_chgrec'), ('view_note2', 'view_note2'), ('view_man', 'view_man'), ('view_cid', 'view_cid'), ('view_addr1', 'view_addr1'), ('view_addr2', 'view_addr2'), ('view_addr3', 'view_addr3'), ('view_addr4', 'view_addr4'), ('view_tel1', 'view_tel1'), ('view_tel2', 'view_tel2'), ('view_tel3', 'view_tel3'), ('view_tel4', 'view_tel4'), ('view_oth1', 'view_oth1'), ('view_oth2', 'view_oth2'), ('view_oth3', 'view_oth3'), ('view_oth4', 'view_oth4'), ('view_download_car_list', 'view_download_car_list')), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
