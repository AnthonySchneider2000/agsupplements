from django.urls import path
from . import views

urlpatterns = [
    path('get-all-items/', views.get_all_items, name='get_all_items'),
    path('create-item/', views.create_item, name='create_item'),
    path('delete-item/<int:id>/', views.delete_item, name='delete_item'),
    path('get-item-by-id/<int:id>/', views.get_item_by_id, name='get_item_by_id'),
    path('update-item/<int:id>/', views.update_item, name='update_item'),
    path('get-all-ingredients/', views.get_all_ingredients, name='get_all_ingredients'),
    path('create-ingredient/', views.create_ingredient, name='create_ingredient'),
    path('delete-ingredient/<int:id>/', views.delete_ingredient, name='delete_ingredient'),
    path('delete-ingredient-by-name/<str:name>/', views.delete_ingredient_by_name, name='delete_ingredient_by_name'),
    path('get-current-table-data/', views.get_current_table_data, name='get_current_table_data'),
    path('blacklist-item/<int:id>/', views.blacklist_item, name='blacklist_item'),
]
