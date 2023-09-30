from django.urls import path
from . import views

urlpatterns = [
    path('get-dummy-data/', views.get_dummy_data, name='get_dummy_data'),
    path('get-item-with-ingredients/', views.get_item_with_ingredients, name='get_item_with_ingredients'),
    path('create-item-with-ingredients/', views.create_item_with_ingredients, name='create_item_with_ingredients'),
    path('delete-item-with-ingredients/<int:id>/', views.delete_item_with_ingredients, name='delete_item_with_ingredients'),
    path('get-item-by-id/<int:id>/', views.get_item_by_id, name='get_item_by_id'),
    path('update-item/<int:id>/', views.update_item, name='update_item'),
    path('get-ingredient/', views.get_ingredient, name='get_ingredient'),
    path('create-ingredient/', views.create_ingredient, name='create_ingredient'),
    path('delete-ingredient/<int:id>/', views.delete_ingredient, name='delete_ingredient'),
    path('delete-ingredient-by-name/<str:name>/', views.delete_ingredient_by_name, name='delete_ingredient_by_name'),
    path('get-current-table-data/', views.get_current_table_data, name='get_current_table_data'),
    path('blacklist-item/<int:id>/', views.blacklist_item, name='blacklist_item'),
]
