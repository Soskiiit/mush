from django.urls import path

from guide import views

urlpatterns = [
    path('', views.guide, name='guide'),
]
