from django.urls import path
from theme import views


urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
]
