import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Ingredient, Item, ItemIngredient, BlacklistedItem
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# Create your views here.

def get_dummy_data(request):
    data = [
        {'id': 1, 'name': 'Item 1', 'description': 'This is item 1', 'price': 4110},
        {'id': 2, 'name': 'Item 2', 'description': 'This is item 2', 'price': 200},
        {'id': 3, 'name': 'Item 3', 'description': 'This is item 3', 'price': 130},
        {'id': 4, 'name': 'Item 4', 'description': 'This is item 4', 'price': 40},
        {'id': 5, 'name': 'Item 5', 'description': 'This is item 5', 'price': 1050},
        {'id': 6, 'name': 'Item 6', 'description': 'This is item 6', 'price': 260},
        {'id': 7, 'name': 'Item 7', 'description': 'This is item 7', 'price': 170},
        {'id': 8, 'name': 'Item 8', 'description': 'This is item 8', 'price': 85},
        {'id': 9, 'name': 'Item 9', 'description': 'This is item 9', 'price': 90},
    ]
    return JsonResponse(data, safe=False)




@csrf_exempt
def create_item_with_ingredients(request):
    #get blacklisted items
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    ingredient_data = data.get('ingredients', [])
    link = data.get('link', '') # optional

    # Check if the item is blacklisted
    if BlacklistedItem.objects.filter(item__name=name).exists():
        return JsonResponse({"message": "Item is blacklisted"})
    
    # Create the ItemWithIngredients instance
    item = Item(name=name, description=description, price=price, link=link)
    item.save()

    # Create ItemIngredient instances for each ingredient and associate them with the item
    for ingredient_info in ingredient_data:
        ingredient_id = ingredient_info.get('id')
        mass = ingredient_info.get('mass')
        ingredient = Ingredient.objects.get(id=ingredient_id)
        item_ingredient = ItemIngredient(item=item, ingredient=ingredient, mass=mass)
        item_ingredient.save()

    return JsonResponse({"message": "Item with ingredients created successfully"})

def get_item_with_ingredients(request): 
    items = Item.objects.all()
    response = []
    for item in items:
        response.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "ingredients": [
                {
                    "id": item_ingredient.ingredient.id,
                    "ingredient": {
                        "id": item_ingredient.ingredient.id,
                        "name": item_ingredient.ingredient.name,
                        "description": item_ingredient.ingredient.description,
                        "price": item_ingredient.ingredient.price
                    },
                    "mass": item_ingredient.mass,
                }
                for item_ingredient in item.itemingredient_set.all()
            ],
            "link": item.link
        })
    return JsonResponse(response, safe=False)

def get_item_by_id(request, id):
    item = Item.objects.get(id=id)
    response = {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "ingredients": [
            {
                "id": item_ingredient.ingredient.id,
                "ingredient": {
                    "id": item_ingredient.ingredient.id,
                    "name": item_ingredient.ingredient.name,
                    "description": item_ingredient.ingredient.description,
                    "price": item_ingredient.ingredient.price
                },
                "mass": item_ingredient.mass,
            }
            for item_ingredient in item.itemingredient_set.all()
        ],
        "link": item.link
    }
    return JsonResponse(response, safe=False)

@csrf_exempt
def update_item(request, id):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    ingredient_data = data.get('ingredients', [])
    link = data.get('link', '') # optional
    
    # retrieve the Item instance
    item = Item.objects.get(id=id)
    
    item_ingredients = item.itemingredient_set.all()
    
    # for all ingredients in the request, modify the ItemIngredient instance
    # if the ItemIngredient instance does not exist, create it
    for ingredient_info in ingredient_data:
        ingredient_id = ingredient_info.get('id')
        mass = ingredient_info.get('mass')
        ingredient = Ingredient.objects.get(id=ingredient_id)
        try:
            item_ingredient = item_ingredients.get(ingredient=ingredient)
            item_ingredient.mass = mass
            item_ingredient.save()
        except ItemIngredient.DoesNotExist:
            item_ingredient = ItemIngredient(item=item, ingredient=ingredient, mass=mass)
            item_ingredient.save()
    
    # modify the Item instance
    item.name = name
    item.description = description
    item.price = price
    item.link = link
    item.save()
    
    return JsonResponse({"message": "Item updated successfully"})

@csrf_exempt
def get_current_table_data(request): #takes a list of selectedIngredients, an array of "conditions" strings, an array of "columns" strings, and returns the new table data
    #a condition may be "ingredient1>ingredient2" etc, "ingredient1>x" etc, "ingredient1=x", "ingredient1!x" 
    #a column may be "ingredient1/ingredient2", "ingredient1/x", "ingredient1/price", etc
    
    data = json.loads(request.body)
    selected_ingredients_data = data.get('selectedIngredients', [])
    selected_ingredients = []
    conditions = data.get('conditions', [])
    columns = data.get('columns', [])
    response = []
    
    for ingredient_data in selected_ingredients_data:
        ingredient_id = ingredient_data.get('id')
        ingredient = Ingredient.objects.get(id=ingredient_id)
        selected_ingredients.append(ingredient)
        
    for item in Item.objects.all():
        itemMeetsAllConditions = True
        item_data = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "link": item.link
        }
        for ingredient in selected_ingredients:
            try:
                # Fetch the related ItemIngredient object
                item_ingredient = item.itemingredient_set.get(ingredient=ingredient)
                ingredientMass = item_ingredient.mass
                item_data[ingredient.name] = ingredientMass
            except ItemIngredient.DoesNotExist:
                itemMeetsAllConditions = False
                break
            
        if not itemMeetsAllConditions:
            continue
            
        for condition in conditions:
            #finds the operator
            for char in condition:
                if char == ">" or char == "<" or char == "=" or char == "!":
                    operator = char
            var1 = condition.split(operator)[0]
            var2 = condition.split(operator)[1]
            
            
            
            #if var1 contains a "/", then it is a column, so we need to find the value of the column
            #else, set var1Comparison to item_data[var1]
            if "/" in var1:
                part1 = var1.split("/")[0]
                part2 = var1.split("/")[1]
                var1Comparison = item_data[part1] / item_data[part2]
            else:
                var1Comparison = item_data[var1]
                
            try:
                var2Comparison = float(var2)
            except ValueError:
                var2Comparison = item_data[var2]
            
            
            if operator == ">":
                if var1Comparison <= var2Comparison:
                    itemMeetsAllConditions = False
                    break
            elif operator == "<":
                if var1Comparison >= var2Comparison:
                    itemMeetsAllConditions = False
                    break
            elif operator == "=":
                if var1Comparison != var2Comparison:
                    itemMeetsAllConditions = False
                    break
            elif operator == "!":
                if var1Comparison == var2Comparison:
                    itemMeetsAllConditions = False
                    break
                
        if not itemMeetsAllConditions:
            continue
                
        for column in columns:
            operator = "/"
            var1 = column.split(operator)[0]
            var2 = column.split(operator)[1]
            item_data[column] = item_data[var1] / item_data[var2]
                
        if itemMeetsAllConditions:
            response.append(item_data)
        
    return JsonResponse(response, safe=False)
        


    
    
@csrf_exempt
def get_filtered_table_data(request): #takes a list of selectedIngredients and a boolean of showCostRatio and returns the new table data
    data = json.loads(request.body)
    selected_ingredients_data = data.get('selectedIngredients', [])
    selected_ingredients = []
    show_cost_ratio = data.get('showCostRatio', False)
    response = []
    
    for ingredient_data in selected_ingredients_data:
        ingredient_id = ingredient_data.get('id')
        ingredient = Ingredient.objects.get(id=ingredient_id)
        selected_ingredients.append(ingredient)
    
    for item in Item.objects.all():
        contains_all_ingredients = True
        item_data = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price
        }
        for ingredient in selected_ingredients:
            try:
                # Fetch the related ItemIngredient object
                item_ingredient = item.itemingredient_set.get(ingredient=ingredient)
                ingredientMass = item_ingredient.mass
                item_data[ingredient.name] = ingredientMass
                if show_cost_ratio:
                    item_data[ingredient.name + " Cost Ratio"] = item.price / ingredientMass
            except ItemIngredient.DoesNotExist:
                contains_all_ingredients = False
                break
        if contains_all_ingredients:
            response.append(item_data)
        
    return JsonResponse(response, safe=False)
    
def get_all_table_data(request):
    items = Item.objects.all()
    response = []
    for item in items:
        response.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "ingredients": [
                {
                    "id": item_ingredient.ingredient.id,
                    "ingredient": {
                        "id": item_ingredient.ingredient.id,
                        "name": item_ingredient.ingredient.name,
                        "description": item_ingredient.ingredient.description,
                        "price": item_ingredient.ingredient.price
                    },
                    "mass": item_ingredient.mass,
                    "costRatio": item_ingredient.ingredient.price / item_ingredient.mass
                }
                for item_ingredient in item.itemingredient_set.all()
            ]
        })
    return JsonResponse(response, safe=False)
        


@csrf_exempt
def delete_item_with_ingredients(request, id):
    item = Item.objects.get(id=id)
    item.delete()

    return JsonResponse({"message": "Item with ingredients deleted successfully"})

@csrf_exempt
def create_ingredient(request):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    ingredient = Ingredient(name=name, description=description, price=price)
    ingredient.save()

    return JsonResponse({"message": "Ingredient created successfully"})

@csrf_exempt
def delete_ingredient(request, id):
    ingredient = Ingredient.objects.get(id=id)
    ingredient.delete()

    return JsonResponse({"message": "Ingredient deleted successfully"})

@csrf_exempt
def delete_ingredient_by_name(request, name):
    ingredient = Ingredient.objects.get(name=name)
    ingredient.delete()

    return JsonResponse({"message": "Ingredient deleted successfully"})


def get_ingredient(request):
    ingredients = Ingredient.objects.all()
    response = []
    for ingredient in ingredients:
        response.append({
            "id": ingredient.id,
            "name": ingredient.name,
            "description": ingredient.description,
            "price": ingredient.price
        })
    return JsonResponse(response, safe=False)


@csrf_exempt
def blacklist_item(request, id):
    item = Item.objects.get(id=id)
    reason = json.loads(request.body).get('reason', '')
    blacklisted_item = BlacklistedItem(item=item, reason=reason)
    blacklisted_item.save()
    item.delete() # delete the item from the database
    return JsonResponse({"message": "Item blacklisted successfully"})