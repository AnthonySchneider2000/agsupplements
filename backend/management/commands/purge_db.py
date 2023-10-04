# backend/management/commands/purge_db.py
from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item


class Command(BaseCommand):
    help = 'Deletes all items and itemingredients from the database'
    
    def handle(self, *args, **kwargs):
        # Delete all items and itemingredients from the database
        ItemIngredient.objects.all().delete()
        Item.objects.all().delete()
        
        print('Deleted all items and itemingredients from the database')