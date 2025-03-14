from django.urls import path
from .views import index, add_item, upload_list, update_status, undo_status, clear_list, clear_history

urlpatterns = [
    path('', index, name='index'),
    path('add/', add_item, name='add_item'),
    path('update-status/', update_status, name='update_status'),
    path('undo-status/', undo_status, name='undo_status'),
    path('upload/', upload_list, name='upload_list'),
    path('clear/', clear_list, name='clear_list'),
    path('clear-history/', clear_history, name='clear_history'),
]
