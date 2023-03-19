# Generated by Django 2.2 on 2023-03-19 13:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username')),
                ('nickname', models.CharField(max_length=254, verbose_name='nickname')),
                ('mobile1', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+()-]+$', 'Enter a valid mobile number.', 'invalid')], verbose_name='mobile number')),
                ('mobile2', models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+()-]+$', 'Enter a valid mobile number.', 'invalid')], verbose_name='mobile number')),
                ('tel1', models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+()-]+$', 'Enter a valid mobile number.', 'invalid')], verbose_name='mobile number')),
                ('tel2', models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+()-]+$', 'Enter a valid mobile number.', 'invalid')], verbose_name='mobile number')),
                ('email1', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('email2', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('email3', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('email4', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('expired_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='expired_date')),
                ('send_sms', models.BooleanField(default=False, verbose_name='send sms')),
                ('send_email', models.BooleanField(default=False, verbose_name='send email')),
                ('note', models.EmailField(blank=True, max_length=254, null=True, verbose_name='note')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create_at')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('type_id', models.IntegerField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=50)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_type_create_at', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_type', to='users.UserType'),
        ),
    ]
