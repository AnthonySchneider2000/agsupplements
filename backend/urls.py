from django.urls import path
from . import views

urlpatterns = [
    path('get-data/', views.get_data, name='get_data'),
    path('create-item/', views.create_item, name='create_item'),
]
