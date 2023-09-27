# backend/management/commands/delete_empty_carbohydrate.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item

# This command will check all Items in the database and delete the ItemIngredient which contains the ingredient "Carbohydrate" if the mass is 0
class Command(BaseCommand):
    help = 'Deletes all ItemIngredients from the database which contain the ingredient "Carbohydrate" and have a value of 0'
    
    def handle(self, *args, **kwargs):
        # get the ingredient object for "Carbohydrate"
        carbohydrate = Ingredient.objects.get(name="Carbohydrate")
        
        # get all ItemIngredients which contain the ingredient "Carbohydrate" and have a mass of 0
        itemIngredients = ItemIngredient.objects.filter(ingredient=carbohydrate, mass=0)
        
        # delete all ItemIngredients which contain the ingredient "Carbohydrate" and have a mass of 0
        itemIngredients.delete()
        
        print('Deleted ' + str(len(itemIngredients)) + ' ItemIngredients from the database which contained the ingredient "Carbohydrate" and had a mass of 0')