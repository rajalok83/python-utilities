from django.contrib import admin

# Register your models here.
from .models import ScheduleConfig, SchedulerLoad, SchedulerProcess

admin.site.register(SchedulerLoad)
admin.site.register(ScheduleConfig)
admin.site.register(SchedulerProcess)
