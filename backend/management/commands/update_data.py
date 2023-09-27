# backend/management/commands/update_data.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item

# This command will delete all items from the database whose id is greater than 204
class Command(BaseCommand):
    help = 'Deletes all items from the database whose id is greater than 204'
    
    def handle(self, *args, **kwargs):
        # get all items whose id is greater than 204
        items = Item.objects.filter(id__gt=204)
        
        # delete all items whose id is greater than 204
        items.delete()
        
        print('Deleted ' + str(len(items)) + ' items from the database whose id is greater than 204')