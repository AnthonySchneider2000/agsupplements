from django.urls import path
from . import views

urlpatterns = [
    path('get-dummy-data/', views.get_dummy_data, name='get_dummy_data'),
    path('create-item/', views.create_item, name='create_item'),
    path('delete-item/<int:id>/', views.delete_item, name='delete_item'),
    path('get-item/', views.get_item, name='get_item'),
    path('get-item-with-ingredients/', views.get_item_with_ingredients, name='get_item_with_ingredients'),
    path('create-item-with-ingredients/', views.create_item_with_ingredients, name='create_item_with_ingredients'),
    path('delete-item-with-ingredients/<int:id>/', views.delete_item_with_ingredients, name='delete_item_with_ingredients'),
    path('get-ingredient/', views.get_ingredient, name='get_ingredient'),
    path('create-ingredient/', views.create_ingredient, name='create_ingredient'),
    path('delete-ingredient/<int:id>/', views.delete_ingredient, name='delete_ingredient'),
]
