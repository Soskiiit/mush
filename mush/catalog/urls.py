from catalog import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path(
        'project/<int:id>/last_update',
        views.project_last_update,
        name='project_last_update'
    ),
    path('project/<int:id>', views.project, name='project'),
    path('project-edit/<int:id>', views.project_edit, name='project-edit'),
    path('project-create/', views.project_create, name='project-create'),
    path(
        'project-delete/<int:id>',
        views.project_delete,
        name='project-delete'
    ),
    path(
        'project-download/<int:id>',
        views.project_download,
        name='project-download'
    ),
]
