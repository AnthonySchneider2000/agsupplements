# backend/management/commands/update_ingredient_prices.py
from django.core.management.base import BaseCommand
from backend.models import ItemIngredient, Ingredient, Item

class Command(BaseCommand):
    help = 'Updates the (default) prices of all ingredients. The price is set to the lowest price/gram of the ingredient in the database'
        
    def handle(self, *args, **kwargs):
        # get all ingredients
        ingredients = Ingredient.objects.all()
        # get all ItemIngredients
        itemIngredients = ItemIngredient.objects.all()
        
        for ingredient in ingredients:
            # get all ItemIngredients which contain the ingredient
            itemIngredientsWithIngredient = itemIngredients.filter(ingredient=ingredient)
            # set lowest price to max value
            lowestPrice = float('inf')
            # if there are no ItemIngredients which contain the ingredient, skip it
            if len(itemIngredientsWithIngredient) == 0:
                continue
            
            for itemIngredient in itemIngredientsWithIngredient:
                parentItem = Item.objects.get(id=itemIngredient.item.id)
                if parentItem.price == 0 or itemIngredient.mass == 0: # if the price or mass is 0, skip it
                    continue
                pricePerGram = parentItem.price / itemIngredient.mass
                if pricePerGram < lowestPrice:
                    lowestPrice = pricePerGram
                    print('New lowest price for ingredient ' + ingredient.name + ' is ' + str(lowestPrice) + ' from item ' + parentItem.name)
            # set the price of the ingredient to the lowest price
            ingredient.price = lowestPrice
            ingredient.save()
            print('Updated price of ingredient ' + ingredient.name + ' to ' + str(ingredient.price))

            