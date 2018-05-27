from django.contrib import admin
from timetable import models

# Register your models here.
admin.site.register(models.Class)
admin.site.register(models.Teacher)
admin.site.register(models.Audience)
admin.site.register(models.Workload)
admin.site.register(models.Subject)
admin.site.register(models.StudyPlan)