# Generated by Django 2.2 on 2023-03-19 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20230319_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='note',
            field=models.TextField(blank=True, max_length=254, null=True, verbose_name='備註'),
        ),
    ]