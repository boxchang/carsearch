# Generated by Django 2.2 on 2023-02-27 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filejob',
            name='batch_no',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
