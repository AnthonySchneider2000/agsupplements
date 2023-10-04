# backend/management/commands/read_from_csv_whole_unit.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item, BlacklistedItem
import csv
import os
import re

class Command(BaseCommand):
    help = 'Reads from csv file and populates database'
    
    # map names to ingredient names
    ingredientNameMap = {
        "Total Fat": "Fat",
        "Saturated Fat": "Saturated Fat",
        "Trans Fat": "Trans Fat",
        "Cholesterol": "Cholesterol",
        "Sodium": "Sodium",
        "Total Carbohydrate": "Carbohydrate",
        "Dietary Fiber": "Fiber",
        "Sugars": "Sugar",
        "Protein": "Protein",
    }
        
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='csv file to read from') # csv file to read from, file must be in same directory as manage.py
        
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        if not os.path.exists(csv_file):
            print('File does not exist')
            return
        
        with open(csv_file) as f:
            reader = csv.reader(f)

            offset = 0
            # if the 3rd column is not category-link, set the header offset to 2
            # this is because this csv is from scraping multiple pages, and the csv contains 2 additional columns
            if next(reader)[3] != 'category-link':
                offset = 2
            
            next(reader) # skip header row
            

            for row in reader:
                name = row[2 + offset]
                
                #check if the item is blacklisted
                if BlacklistedItem.objects.filter(item__name=name).exists():
                    print('Item ' + name + ' is blacklisted')
                    continue
                
                # if an item with the same name already exists, skip it
                if Item.objects.filter(name=name).exists():
                    print('Item ' + name + ' already exists')
                    continue
                
                # in the form $12.47
                price = row[4 + offset]
                if price == '':
                    print('Item ' + name + ' does not have a price')
                    continue
                price = re.sub("[^0-9.]", "", price) # remove non-numeric characters
                if float(price) <= 0:
                    print('Item ' + name + ' has a price of 0')
                    continue
                price = float(price)
                
                
                #if the servingSize is not empty, use that, otherwise use servingSize2
                servingCount = row[5 + offset] if row[5 + offset] else row[6 + offset]
                if " Servings" not in servingCount:
                    print('Item ' + name + ' does not have Servings')
                    continue
                #remove non-numeric characters
                servingCount = re.sub("[^0-9.]", "", servingCount)
                servingCount = float(servingCount)

                link = row[3 + offset]
                
                
                calories = row[7 + offset]
                
                # if calories is non numeric or 0, skip it
                if not calories or not calories.isnumeric() or float(calories) == 0:
                    print('Item ' + name + ' does not have calories')
                    continue
                
                calories = float(calories) * servingCount # multiply by servings per pound
                
                print("\nCreating item " + name + " with price " + price + " description " + name + " link " + link + " and calories " + str(calories) + " and servings per pound " + str(servingCount))
                item = Item.objects.create(name=name, price=price, description=name, link=link, servings=servingCount)

                calorie_ingredient = Ingredient.objects.get(name='Calories')
                calorie_item_ingredient = ItemIngredient.objects.create(item=item, ingredient=calorie_ingredient, mass=calories)
                
                # split macros into a list of strings
                macros = row[8 + offset].split('%')
                
                
                # remove empty strings
                macros = list(filter(None, macros))
                
                for macro in macros:
                    # parse macro string until it stops matching anything in the ingredientNameMap
                    for key in self.ingredientNameMap: # iterate through the keys in the map
                        if key in macro: # if the key is in the macro string
                            # get the ingredient name from the map
                            ingredientName = self.ingredientNameMap[key]
                            afterIngredientName = macro.split(key)[1] # split on the key and take the second element
                            # remove anything after g
                            afterIngredientName = afterIngredientName.split('g')[0] + "g"
                            # remove spaces
                            afterIngredientName = afterIngredientName.replace(" ", "")
                            # numeric value of the ingredient
                            match = re.match(r'(\d+\.?\d*)\s*(\w+)', afterIngredientName) # match a number followed by a word
                            if match:
                                ingredientAmount = match.group(1) # get the first group, which is the number
                                ingredientAmount = re.sub("[^0-9.]", "", ingredientAmount) # remove non-numeric characters
                                ingredientAmount = float(ingredientAmount)
                                ingredientUnits = match.group(2) # get the second group, which is the units
                            else:
                                ingredientAmount = None
                                ingredientUnits = None
                                
                            # convert values to grams if necessary
                            if ingredientUnits == 'mg':
                                ingredientAmount /= 1000
                                ingredientUnits = 'g'
                                
                            if ingredientAmount is not None:
                                if ingredientAmount > 0: # if the ingredient amount is 0, skip it
                                    ingredientAmount *= servingCount # multiply by servings per pound
                                    print("    Item " + name + " has " + str(ingredientAmount) + " grams of " + ingredientName)
                                    ingredient = Ingredient.objects.get(name=ingredientName) # get the ingredient object
                                    item_ingredient = ItemIngredient.objects.create(item=item, ingredient=ingredient, mass=ingredientAmount) # create the item ingredient         
                                
                                
                            
        print('Done')