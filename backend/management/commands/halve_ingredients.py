# backend/management/commands/halve_ingredients.py

from django.core.management.base import BaseCommand
from backend.models import ItemIngredient, Ingredient, Item

# This command will halve the mass of all ItemIngredients in the item with the argument id

class Command(BaseCommand):
    help = 'Halves the mass of all ItemIngredients in the item with the argument id'
    
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='id of the item to halve the ingredients of')
        
    def handle(self, *args, **kwargs):
        id = kwargs['id']
        
        # get the item
        item = Item.objects.get(id=id)
        
        # get all ItemIngredients in the item
        itemIngredients = ItemIngredient.objects.filter(item=item)
        
        # halve the mass of all ItemIngredients in the item
        for itemIngredient in itemIngredients:
            itemIngredient.mass /= 2
            itemIngredient.save()
        
        print('Halved the mass of all ItemIngredients in the item with id ' + str(id))