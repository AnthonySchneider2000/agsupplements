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
            # example data
            # web-scraper-order,web-scraper-start-url,category-link,category-link-href,price,servingSize,servingSize2,Calories,Macros
            # 1695697305-1,https://www.walmart.com/search?q=steak,"Beef Choice Angus Tomahawk Ribeye Steak Bone-In, 1.68 - 3.22 lb Tray",https://www.walmart.com/ip/Beef-Choice-Angus-Tomahawk-Ribeye-Steak-Bone-In-1-68-3-22-lb-Tray/331823702?from=/search,$12.47 ,5  Servings Per Container,3.95 oz (112 g),290,Total Fat 23g35%Saturated Fat9g45%Cholesterol 85mg28%Sodium 55mg2%Total Carbohydrate 0g0%Protein 21g0%
            next(reader) # skip header row

            for row in reader:
                name = row[2]
                
                if Item.objects.filter(name=name).exists():
                    print('Item with name ' + name + ' already exists')
                    continue
                
                price = row[4][1:].strip() #trim dollar sign and space, price per pound
                
                #if the servingSize2 is not empty, use that, otherwise use servingSize
                servingSize = row[6] if row[6] else row[5]
                #trim the serving size to just the number (oz)
                servingSize = servingSize.split()[0] # split on space and take first element
                
                servingsPerPound = 16 / float(servingSize) # 16 oz in a pound
                
                item = Item.objects.create(name=name, price=price, description=name)
                
                calories = row[7]
                
                
                calorie_ingredient = Ingredient.objects.get(name='Calories')
                calorie_item_ingredient = ItemIngredient.objects.create(item=item, ingredient=calorie_ingredient, mass=calories)
                
                # split macros into a list of strings
                macros = row[8].split('%')
                
                
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
                                
                            ingredient = Ingredient.objects.get(name=ingredientName)
                            item_ingredient = ItemIngredient.objects.create(item=item, ingredient=ingredient, mass=ingredientAmount)         
        print('Done')