from django.urls import path
from theme import views


urlpatterns = [
    path('', views.CatalogView.as_view(), name='index'),
    path('projects/', views.MyProjectsView.as_view(), name='my-projects'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('item/', views.ItemDetailsView.as_view(), name='item'),
    path('edit/', views.ItemEditView.as_view(), name='edit'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path(
        'profile-edit/',
        views.ProfileEditView.as_view(),
        name='profile-edit'
    ),
]
