# Generated by Django 2.2 on 2023-03-09 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_car_batch_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='id',
        ),
        migrations.AlterField(
            model_name='car',
            name='CARNO',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
