# Generated by Django 2.2 on 2023-04-11 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0008_car2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='CHGREC',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='car2',
            name='CHGREC',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='cartemp',
            name='CHGREC',
            field=models.CharField(max_length=255),
        ),
    ]
