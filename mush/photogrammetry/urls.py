from django.urls import path

from . import views

app_name = 'photogrammetry'

urlpatterns = [
    path('', views.run_process, name='run_process'),
]
