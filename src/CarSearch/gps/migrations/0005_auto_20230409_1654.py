# Generated by Django 2.2 on 2023-04-09 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gps', '0004_auto_20230409_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gps_photo',
            name='create_at',
        ),
        migrations.RemoveField(
            model_name='gps_photo',
            name='create_by',
        ),
    ]
