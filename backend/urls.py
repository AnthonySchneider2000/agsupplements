from django.urls import path
from . import views

urlpatterns = [
    path('get-dummy-data/', views.get_dummy_data, name='get_dummy_data'),
    path('create-item/', views.create_item, name='create_item'),
    path('delete-item/<int:id>/', views.delete_item, name='delete_item'),
    path('get-item/', views.get_item, name='get_item'),
]
