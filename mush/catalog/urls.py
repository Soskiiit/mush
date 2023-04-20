from catalog import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:id>', views.project, name='project'),
    path('project-edit/<int:id>', views.project_edit, name='project-edit'),
    path('project-create/', views.project_create, name='project-create'),
    path(
        'project-download/<int:id>',
        views.project_download,
        name='project-download'
    ),
]
