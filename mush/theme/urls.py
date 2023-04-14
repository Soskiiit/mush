from django.urls import path
from theme import views


urlpatterns = [
    path('', views.ItemDetailsView.as_view(), name='item'),
    path('edit/', views.ItemEditView.as_view(), name='edit'),
]
