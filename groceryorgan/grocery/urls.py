from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_item, name='add_item'),
    path('update-status/', views.update_status, name='update_status'),
    path('upload/', views.upload_list, name='upload_list'),
]
