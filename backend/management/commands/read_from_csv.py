# backend/management/commands/read_from_csv.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item
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
                
                # if an item with the same name already exists, skip it
                if Item.objects.filter(name=name).exists():
                    print('Item ' + name + ' already exists')
                    continue
                
                # may be of the form $12.47/ea or $12.47/lb, remove $ and /lb, and continue if /lb is not in the string
                price = row[4 + offset]
                if '/lb' in price:
                    price = price.split('/lb')[0].strip()
                    price = price.split('$')[1].strip()
                elif '/oz' in price:
                    price = price.split('/oz')[0].strip()
                    price = price.split('$')[1].strip()
                    price = float(price) * 16 # convert to price per pound
                else:
                    print('Item ' + name + ' does not have /lb in price')
                    continue
                
                #if the servingSize is not empty, use that, otherwise use servingSize2
                servingSize = row[5 + offset] if row[5 + offset] else row[6 + offset]
                # remove oz; if oz is not in the string, continue
                if 'oz' not in servingSize:
                    print('Item ' + name + ' does not have oz in serving size')
                    continue
                servingSize = servingSize.split('oz')[0].strip() # split on oz and take the first element
                
                

                link = row[3 + offset]
                
                servingsPerPound = 16 / float(servingSize) # 16 oz in a pound
                
                calories = row[7 + offset]
                
                if calories == '':
                    print('Item ' + name + ' does not have calories')
                    continue
                
                calories = float(calories) * servingsPerPound # multiply by servings per pound
                
                print("\nCreating item " + name + " with price " + price + " description " + name + " link " + link + " and calories " + str(calories) + " and servings per pound " + str(servingsPerPound))
                item = Item.objects.create(name=name, price=price, description=name, link=link)

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
                                ingredientAmount = float(match.group(1))
                                ingredientUnits = match.group(2)
                            else:
                                ingredientAmount = None
                                ingredientUnits = None
                                
                            # convert values to grams if necessary
                            if ingredientUnits == 'mg':
                                ingredientAmount /= 1000
                                ingredientUnits = 'g'
                                
                            ingredientAmount *= servingsPerPound # multiply by servings per pound
                            print("    Item " + name + " has " + str(ingredientAmount) + " grams of " + ingredientName)
                            
                            if ingredientAmount <= 0: # if the ingredient amount is 0, skip it
                                ingredient = Ingredient.objects.get(name=ingredientName) # get the ingredient object
                                item_ingredient = ItemIngredient.objects.create(item=item, ingredient=ingredient, mass=ingredientAmount) # create the item ingredient         
                                
                                
                            
        print('Done')