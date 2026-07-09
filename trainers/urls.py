from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/',
         views.trainer_dashboard,
         name='trainer_dashboard'),

    path('members/',
         views.trainer_members,
         name='trainer_members'),

    path('attendance/',
         views.mark_attendance,
         name='mark_attendance'),

    path('workout/',
         views.trainer_workout,
         name='trainer_workout'),

    path('upload/',
         views.upload_content,
         name='upload_content'),

    path('progress/',
         views.trainer_progress,
         name='trainer_progress'),
]