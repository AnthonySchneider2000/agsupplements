# backend/management/commands/delete_empty_ingredient.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item

# This command deletes all itemingredients from the database whose mass is <= 0
class Command(BaseCommand):
    help = 'Deletes all itemingredients from the database whose mass is <= 0'
    
    def handle(self, *args, **kwargs):
        # get all itemingredients whose mass is <= 0
        itemIngredients = ItemIngredient.objects.filter(mass__lte=0)
        
        for itemIngredient in itemIngredients:
            parentItem = Item.objects.get(id=itemIngredient.item.id)
            ingredientName = Ingredient.objects.get(id=itemIngredient.ingredient.id).name
            print('Deleted ingredient ' + ingredientName + ' from item ' + parentItem.name + ' because its mass is ' + str(itemIngredient.mass))
        
        # delete all itemingredients whose mass is <= 0
        itemIngredients.delete()
        
        