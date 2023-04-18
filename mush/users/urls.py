from django.urls import path
from users import views


urlpatterns = [
    path('edit-my-profile/', views.edit_my_profile, name='edit-my-profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
]
