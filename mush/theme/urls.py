from django.urls import path
from theme import views


urlpatterns = [
    path('', views.CatalogView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('item/', views.ItemDetailsView.as_view(), name='item'),
    path('edit/', views.ItemEditView.as_view(), name='edit'),
]
