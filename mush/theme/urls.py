from django.urls import path
from theme import views


urlpatterns = [
    path('', views.catalog, name='index'),

    path('projects/', views.projects, name='my-projects'),
    path('project/<int:id>', views.project, name='project'),
    path('project-edit/<int:id>', views.project_edit, name='project-edit'),

    path('user/<int:id>', views.user, name='user'),
    path('profile/', views.profile, name='profile'),
    path('profile-edit/', views.profile_edit, name='profile-edit'),
]
