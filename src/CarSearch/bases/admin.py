from django.contrib import admin
from car.models import CarStatus
from jobs.models import JobStatus
from users.models import UserType


@admin.register(JobStatus)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_en', 'status_cn', 'status_desc')


@admin.register(CarStatus)
class CarStatusAdmin(admin.ModelAdmin):
    list_display = ('status_en', 'status_cn', 'status_desc')


@admin.register(UserType)
class CarStatusAdmin(admin.ModelAdmin):
    list_display = ('type_name',)
