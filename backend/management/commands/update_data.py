# backend/management/commands/update_data.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item

# This command will delete all items from the database which contain the ingredient "Calories"
class Command(BaseCommand):
    help = 'Deletes all items from the database which contain the ingredient "Calories"'
    
    def handle(self, *args, **kwargs):
        # get the ingredient object for "Calories"
        calories = Ingredient.objects.get(name="Calories")
        
        # get all items which contain the ingredient "Calories"
        items = Item.objects.filter(ingredients=calories)
        
        # delete all items which contain the ingredient "Calories"
        items.delete()
        
        print('Deleted ' + str(len(items)) + ' items from the database which contained the ingredient "Calories"')