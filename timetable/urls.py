from django.urls import path
from timetable import views

urlpatterns = [
    path('createSpecSchedule', views.create_special_schedule, name="create_special_schedule"),
    path('createFixSchedule', views.create_fixed_schedule, name="create_fixed_schedule"),
    path('saveScheduele', views.save_schedule, name="save_schedule"),
    path('editScheduele', views.edit_schedule, name="edit_schedule"),
    path('', views.index, name="index"),
]
