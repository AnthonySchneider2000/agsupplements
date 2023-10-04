# backend/management/commands/delete_duplicate_itemingredient.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item

class Command(BaseCommand):
    help = 'Deletes all itemingredients from the database whose parent items contain duplicate ingredients'
    
    def handle(self, *args, **kwargs):
        # Get all items from the database
        items = Item.objects.all()
        
        # Loop through each item
        for item in items:
            # Get all itemingredients for this item
            itemIngredients = ItemIngredient.objects.filter(item=item)
            
            for itemIngredient in itemIngredients:
                # Get all itemingredients for this item whose ingredient is the same as the current itemingredient's ingredient
                duplicateItemIngredients = ItemIngredient.objects.filter(item=item, ingredient=itemIngredient.ingredient)
                
                # If there is more than one itemingredient with the same ingredient, delete the duplicates
                if len(duplicateItemIngredients) > 1:
                    # Delete all itemingredients except the first one
                    for duplicateItemIngredient in duplicateItemIngredients[1:]:
                        duplicateItemIngredient.delete()
                        
                    # Print a message to the console
                    print('Deleted duplicate itemingredient ' + str(duplicateItemIngredient.id) + ' from item ' + item.name)
                
            