# backend/management/commands/read_from_csv_unified.py

from django.core.management.base import BaseCommand
from backend.models import Ingredient, ItemIngredient, Item, Tag, BlacklistedItem
import csv
import os
import re # regular expressions
import pint 

class Command(BaseCommand):
    help = 'Reads from csv file and populates database'
    
    # map names to ingredient names
    ingredientNameMap = {
        "Calories": "Calories",
        "Protein": "Protein",
        "Total Fat": "Fat",
        "Saturated Fat": "Saturated Fat",
        "Trans Fat": "Trans Fat",
        "Cholesterol": "Cholesterol",
        "Sodium": "Sodium",
        "Total Carbohydrate": "Carbohydrate",
        "Dietary Fiber": "Fiber",
        "Sugars": "Sugars",
        "Added Sugars": "Added Sugars",
        "Includes Added Sugars": "Added Sugars",
        "Vitamin A": "Vitamin A",
        "Vitamin C": "Vitamin C",
        "Vitamin D": "Vitamin D",
        "Calcium": "Calcium",
        "Iron": "Iron",
        "Potassium": "Potassium",
        "Niacin": "Niacin",
        "Thiamin": "Thiamin",
        "Vitamin B6": "Vitamin B6",
        "Folate": "Folate",
        "Magnesium": "Magnesium",
        "Riboflavin": "Riboflavin",
        "Folic Acid": "Folic Acid",
        "Selenium": "Selenium",
    }
    
    acceptedUnits = ['oz', 'g', 'mg', 'ug', 'lb', 'kg', '']
    
    validData = True
    name = ''
    price = 0
    price_units = ''
    link = ''
    servingString = ''
    servingCount = 0
    servingUnits = ''
    ingredientNames = []
    ingredientValues = []
    macroNames = []
    microNames = []
    macroValues = []
    microValues = []
    tags = []
    id = 0
    
    
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='csv file to read from') # csv file to read from, file must be in same directory as manage.py
        parser.add_argument('--tags', nargs='+', type=str, help='tags to add to the items') # tags to add to the items
        # example usage: python manage.py read_from_csv_unified <csv_file> --tags <tag1> <tag2> <tag3>
        
        
    def handle(self, *args, **kwargs):
        
        if kwargs['tags']: # if tags were passed in
            self.tags = kwargs['tags'] # set the tags
            for tag in self.tags: # for each tag
                if not Tag.objects.filter(name=tag).exists(): # if the tag does not exist, create it
                    Tag(name=tag).save()
        
        csv_file = kwargs['csv_file']
        if not os.path.exists(csv_file):
            print('File does not exist')
            return
        
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            
            for row in reader: # for each row in the csv file
                #BUG: for some reason "web-scraper-order" is being read as "ï»¿web-scraper-order"
                webScraperOrderHeader = 'ï»¿web-scraper-order'
                if self.id != float(row[webScraperOrderHeader].split('-')[0]): # if the id is different, then we are on a new item
                    
                    if self.id != 0 and self.validData: # save the previous item, if it exists
                        self.save_item()
                        
                    self.reset_variables() # reset variables
                    
                    self.id = float(row[webScraperOrderHeader].split('-')[0])
                    self.parse_basic_data(row)
                    if not self.validData: # if the data is not valid, skip this item
                        continue
                    if row["macro-title"]:
                        self.macroNames.append(row["macro-title"])
                    elif row["micro-title"]:
                        self.microNames.append(row["micro-title"])
                    
                else: 
                    if not self.validData:
                        continue
                    self.parse_ingredients(row)
                    
            self.save_item() # save the last item
                    
                        
                
    def save_item(self):        
        
        if Item.objects.filter(name=self.name).exists():
            print('Item ' + self.name + ' already exists')
            return
        
        # save the item
        item = Item(name=self.name, description=self.name, price=self.price, link=self.link, servings=self.servingCount)
        item.save()
        print('Saved item ' + self.name + ' with price ' + str(self.price) + ' and servings ' + str(self.servingCount)) 
        
        
        for i in range(len(self.macroNames)):
            self.ingredientNames.append(self.macroNames[i])
            self.ingredientValues.append(self.macroValues[i])
            
        for i in range(len(self.microNames)):
            self.ingredientNames.append(self.microNames[i])
            self.ingredientValues.append(self.microValues[i])
        
        
        
        # save the itemingredients
        for i in range(len(self.ingredientNames)):
            # if the ingredient is not in the ingredientNameMap, skip it
            if self.ingredientNames[i] not in self.ingredientNameMap:
                print('    Ingredient ' + self.ingredientNames[i] + ' is not in the ingredientNameMap')
                continue
            ingredientName = self.ingredientNameMap[self.ingredientNames[i]]
            ingredientValueAndUnits = str(self.ingredientValues[i])
            ingredient = Ingredient.objects.get(name=ingredientName)
            ingredientValue = re.sub("[^0-9.]", "", ingredientValueAndUnits) # remove non-numeric characters
            if ingredientValue == '':
                print('    Ingredient ' + ingredientName + ' has no value')
                continue
            ingredientValue = float(ingredientValue)
            ingredientValue = abs(ingredientValue) # sometimes a - ends up in the ingredient value, so we take the absolute value
            ingredientUnits = re.sub("[^a-zA-Z]", "", ingredientValueAndUnits) # remove non-alphabetic characters
            ingredientUnits = ingredientUnits.lower()
            
            # if the ingredient units starts with mc, change it to u, otherwise leave it alone
            if ingredientUnits.startswith('mc'):
                ingredientUnits = 'u' + ingredientUnits[2:]
            # if the ingredient is grm, change it to g, otherwise leave it alone
            if ingredientUnits == 'grm':
                ingredientUnits = 'g'
            
            if ingredientUnits not in self.acceptedUnits: #if the ingredient units is not in the accepted units, skip it
                print('    Ingredient ' + ingredientName + ' has invalid units ' + ingredientUnits)
                continue
            
            desired_units = ingredient.units
            
            if ingredientUnits == '' and desired_units != '':
                print('    Ingredient ' + ingredientName + ' has no units but desired units are ' + desired_units + '. SKIPPING')
                # TODO: consider setting ingredientUnits to desired_units
                continue
                
            
            # if the ingredient units is not the same as the desired units, convert it
            if ingredientUnits != desired_units:
                print('    Ingredient ' + ingredientName + ' has units ' + ingredientUnits + ' but desired units are ' + desired_units)
                
                # use pint to convert the ingredient value to the desired units
                ureg = pint.UnitRegistry()
                ingredientUnits = ureg(ingredientUnits)
                ingredientUnits = ingredientUnits.to(desired_units)
                ingredientUnits = float(ingredientUnits.magnitude)
                ingredientValue = ingredientValue * ingredientUnits
            
            # if the ingredient value is 0, skip it
            if ingredientValue == 0:
                print('    Ingredient ' + ingredientName + ' has a value of 0. SKIPPING')
                continue
            
            ingredientValue *= self.servingCount # multiply by servings per pound
            
            itemIngredient = ItemIngredient(item=item, ingredient=ingredient, mass=ingredientValue)
            itemIngredient.save()
            print("    Added ingredient " + ingredientName + " with mass " + str(ingredientValue) + " " + desired_units + " to item " + self.name)
            
        # save the tags, self.tags is a list of tag names
        for tag in self.tags:
            tag = Tag.objects.get(name=tag)
            item.tags.add(tag)
            print("    Added tag " + tag.name + " to item " + self.name)
        
    
    def reset_variables(self):
        self.validData = True
        self.name = ''
        self.price = 0
        self.link = ''
        self.servingString = ''
        self.servingCount = 0
        self.servingUnits = ''
        self.ingredientNames = []
        self.ingredientValues = []
        self.macroNames = []
        self.microNames = []
        self.macroValues = []
        self.microValues = []
    
    def parse_basic_data(self, row):
        # remove items with no name
        if row['item-link'] == '':
            print('Item has no name')
            self.validData = False
            return 
        else:
            self.name = row['item-link']
            
        self.link = row['item-link-href']
        
        caloriesValue = row['calories']
        if caloriesValue == '':
            print('Item ' + self.name + ' has no calories')
            self.validData = False
            return
        #remove non-numeric characters
        caloriesValue = re.sub("[^0-9.]", "", caloriesValue)
        caloriesValue = float(caloriesValue)
        
        if caloriesValue == 0:
            print('Item ' + self.name + ' has 0 calories')
            self.validData = False
            return
        
        self.ingredientNames.append('Calories')
        self.ingredientValues.append(caloriesValue)
        
        #check if the item is blacklisted
        if BlacklistedItem.objects.filter(item__name=self.name).exists():
            print('Item ' + self.name + ' is blacklisted')
            self.validData = False
            return
        
        isWholeUnit = True # assume the item is a whole unit
        
        if row['avg-price'] == 'avg price': # determine if the item is a whole unit or priced by weight
            isWholeUnit = False
            
        if isWholeUnit:
            #THE ITEM IS A WHOLE UNIT
            self.parse_whole_unit(row)
        else:
            #THE ITEM IS PRICED BY WEIGHT
            self.parse_unit_by_weight(row)
    
    def parse_ingredients(self, row):
        if row["macro-title"]:
            self.macroNames.append(row["macro-title"])
        elif row["micro-title"]:
            self.microNames.append(row["micro-title"])
        else:
            # if macro/micro value array is shorter than its name array, add to it
            # if the value is empty, add "0g"
            if len(self.macroValues) < len(self.macroNames):
                if row["macro-value"]:
                    self.macroValues.append(row["macro-value"])
                else:
                    self.macroValues.append("0g")
            if len(self.microValues) < len(self.microNames):
                if row["micro-value"]:
                    self.microValues.append(row["micro-value"])
                else:
                    self.microValues.append("0g")
        
                    
    def parse_whole_unit(self, row): # THE ITEM IS A WHOLE UNIT
        self.price = row['price']
        self.price = re.sub("[^0-9.]", "", self.price) # remove non-numeric characters
        if self.price == '':
            print('Item ' + self.name + ' does not have a price')
            self.validData = False
            return
        if float(self.price) <= 0:
            print('Item ' + self.name + ' has a price of 0')
            self.validData = False
            return
        self.price = float(self.price)     
        #if serving-size1 is not empty, use that, otherwise use serving-size2
        self.servingString = row['serving-size1'] if row['serving-size1'] else row['serving-size2']
        if " Servings" not in self.servingString:
            print('Item ' + self.name + ' does not have Servings')
            self.validData = False
            return
        self.servingCount = re.sub("[^0-9.]", "", self.servingString)
        self.servingCount = float(self.servingCount)
        
        if self.servingCount == 0:
            print('Item ' + self.name + ' has 0 servings')
            self.validData = False
            return
        
        
        return       
    
    def parse_unit_by_weight(self, row): # THE ITEM IS PRICED BY WEIGHT
        self.price = row['weight-price']
        if "/" not in self.price:
            print('Item ' + self.name + ' does not have / in price')
            self.validData = False
            return
        print('Item ' + self.name + ' has price ' + self.price)
        price_units = self.price.split('/')[1].strip()
        self.price = self.price.split('/')[0].strip()
        self.price = re.sub("[^0-9.]", "", self.price) # remove non-numeric characters
        self.price = float(self.price)
        price_units = re.sub("[^a-zA-Z]", "", price_units) # remove non-alphabetic characters
        
        #if serving-size2 is not empty, use that, otherwise use serving-size1
        self.servingString = row['serving-size2'] if row['serving-size2'] else row['serving-size1']
        self.servingString = str(self.servingString).lower()
        # if servingString does not contain any of the accepted units, skip it
        if not any(unit in self.servingString for unit in self.acceptedUnits):
            print('Item ' + self.name + ' does not have any accepted units in serving size')
            self.validData = False
            return
        #strip everything after the first accepted unit
        #ex. 4 oz (112 g)  Serving Size should cut after oz, not g
        for unit in self.acceptedUnits:
            if unit in self.servingString:
                self.servingString = self.servingString.split(unit)[0].strip()
                #include the unit in the serving string
                self.servingString += unit
                break
        #at this point servingString should be a number followed by a unit
        print('Item ' + self.name + ' has serving size ' + self.servingString)
        self.servingCount = re.sub("[^0-9.]", "", self.servingString) # remove non-numeric characters
        self.servingCount = float(self.servingCount)
        self.servingUnits = re.sub("[^a-zA-Z]", "", self.servingString) # remove non-alphabetic characters
        # ex. servingCount = 1.5, servingUnits = oz
        # update servingCount to be the servings in 1 price_units (ex. 1 lb)
        servings = 1
        if price_units == "lb" and self.servingUnits == "oz":
            servings = 16 / self.servingCount
        elif price_units == "oz" and self.servingUnits == "lb":
            servings = (1/self.servingCount) / 16
        elif price_units == "lb" and self.servingUnits == "g":
            servings = 453.592 / self.servingCount
        elif price_units == "g" and self.servingUnits == "lb":
            servings = (1/self.servingCount) / 453.592
        elif price_units == "lb" and self.servingUnits == "lb":
            servings = (1/self.servingCount)
        elif price_units == "oz" and self.servingUnits == "oz":
            servings = (1/self.servingCount)
        elif price_units == "g" and self.servingUnits == "g":
            servings = (1/self.servingCount)
        else:
            print('Item ' + self.name + ' has invalid serving/price units: ' + str(self.servingUnits) + '/' + str(price_units))
            self.validData = False
            return

        self.servingCount = servings
        
        if self.servingCount == 0:
            print('Item ' + self.name + ' has 0 servings')
            self.validData = False
            return
        
        return
    
        
    