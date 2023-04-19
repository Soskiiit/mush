from django.urls import path

from . import views

app_name = 'photogrammetry'

urlpatterns = [
    path(
        'compute/<int:model_id>/',
        views.run_photogrammetry,
        name='run_process',
    ),
]
