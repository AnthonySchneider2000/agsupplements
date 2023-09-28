# backend/management/commands/change_serving_count.py
from django.core.management.base import BaseCommand
from backend.models import ItemIngredient, Ingredient, Item
from decimal import Decimal

class Command(BaseCommand):
    help = 'Changes the macros of an item, by given id, based on the input: previous serving count, new serving count'
    
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='id of the item to halve the ingredients of')
        parser.add_argument('previous_serving_count', type=int, help='previous serving count')
        parser.add_argument('new_serving_count', type=int, help='new serving count')
    #an example usage of this command is: python manage.py change_serving_count 1 1 2
        
    def handle(self, *args, **kwargs):
        id = kwargs['id']
        previous_serving_count = kwargs['previous_serving_count']
        new_serving_count = kwargs['new_serving_count']
        
        # get the item
        item = Item.objects.get(id=id)
        
        servingRatio = new_serving_count / previous_serving_count
        
        
        # get all ItemIngredients in the item
        itemIngredients = ItemIngredient.objects.filter(item=item)
        
        # halve the mass of all ItemIngredients in the item
        for itemIngredient in itemIngredients:
            itemIngredient.mass *= Decimal(servingRatio)
            itemIngredient.save()
        
        print('Changed the serving count of ' + item.name + ' from ' + str(previous_serving_count) + ' to ' + str(new_serving_count))