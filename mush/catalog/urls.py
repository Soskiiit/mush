from catalog import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:id>', views.project, name='project'),
    path('project-edit/<int:id>', views.project_edit, name='project-edit'),
]
