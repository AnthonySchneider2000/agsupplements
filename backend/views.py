import json
import time
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Ingredient, Item, ItemIngredient, BlacklistedItem, Tag
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# Create your views here.

@csrf_exempt
def create_item(request):
    #get blacklisted items
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    ingredient_data = data.get('ingredients', [])
    link = data.get('link', '') # optional
    servings = data.get('servings', None) # optional
    tags = data.get('tags', []) # optional

    # Check if the item is blacklisted
    if BlacklistedItem.objects.filter(item__name=name).exists():
        return JsonResponse({"message": "Item is blacklisted"})
    
    # Create the Item instance
    item = Item(name=name, description=description, price=price, link=link, servings=servings)
    item.save()

    # Create ItemIngredient instances for each ingredient and associate them with the item
    for ingredient_info in ingredient_data:
        ingredient_id = ingredient_info.get('id')
        mass = ingredient_info.get('mass')
        if mass == 0: # if the mass is 0, don't create an ItemIngredient instance
            continue
        ingredient = Ingredient.objects.get(id=ingredient_id)
        item_ingredient = ItemIngredient(item=item, ingredient=ingredient, mass=mass*float(servings))
        item_ingredient.save()
        
    for tag_name in tags:
        if not Tag.objects.filter(name=tag_name).exists():
            tag = Tag(name=tag_name)
            tag.save()
        tag = Tag.objects.get(name=tag_name)
        item.tags.add(tag)

    return JsonResponse({"message": "Item created successfully"})

def get_all_items(request): 
    items = Item.objects.all()
    response = []
    for item in items:
        response.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "servings": item.servings,
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
        "servings": item.servings,
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
    servings = data.get('servings', None) # optional
    tags = data.get('tags', []) # optional
    
    # retrieve the Item instance
    item = Item.objects.get(id=id)
    
    item_ingredients = item.itemingredient_set.all()
    
    for item_ingredient in item_ingredients:
        print("item_ingredient: " + str(item_ingredient.ingredient.name) + " in item: " + str(item.name))
    
    # if servings is not None, update the mass of each ItemIngredient instance
    if servings is not None and float(servings) != float(item.servings):
        print("changing servings from " + str(item.servings) + " to " + str(servings))
        for item_ingredient in item_ingredients:
            print("changing mass of item_ingredient: " + str(item_ingredient.ingredient.name) + " in item: " + str(item.name) + " from " + str(item_ingredient.mass) + " to " + str(float(item_ingredient.mass) / float(item.servings) * float(servings)) + " grams")
            item_ingredient.mass = float(item_ingredient.mass) / float(item.servings) * float(servings)
            item_ingredient.save()
    
    # for all ingredients in the request, modify the ItemIngredient instance
    # if the ItemIngredient instance does not exist, create it
    for ingredient_info in ingredient_data:
        print("ingredient_info: ")
        print(ingredient_info)
        ingredient_id = ingredient_info.get('id')
        mass = float(ingredient_info.get('mass')) * float(servings)
        ingredient = Ingredient.objects.get(id=ingredient_id)
        if servings is not None and float(servings) != float(item.servings):
            print("servings has changed")
            try:
                print("serving count changed from " + str(item.servings) + " to " + str(servings) + ", changing mass of ingredient: " + str(ingredient.name) + " in item: " + str(item.name) + " from " + str(mass) + " to " + str(float(mass) / float(item.servings) * float(servings)) + " grams")
                item_ingredient = item_ingredients.get(ingredient=ingredient)
                item_ingredient.mass = float(item_ingredient.mass) / float(item.servings) * float(servings)
                item_ingredient.save()
            except ItemIngredient.DoesNotExist:
                pass
            if item_ingredient.mass == 0:
                item_ingredient.delete()
            continue # skip the rest of the loop
        try:
            item_ingredient = item_ingredients.get(ingredient=ingredient)
            print("ItemIngredient exists, modifying item_ingredient: " + str(ingredient.name) +" in item: " + str(item.name) + " from " + str(item_ingredient.mass) + " to " + str(mass) + " grams")
            item_ingredient.mass = mass
            item_ingredient.save()
        except ItemIngredient.DoesNotExist:
            print("ItemIngredient does not exist, creating item_ingredient: " + str(ingredient.name) +" in item: " + str(item.name))
            item_ingredient = ItemIngredient(item=item, ingredient=ingredient, mass=mass)
            item_ingredient.save()
        # if the mass of the ItemIngredient instance is 0, delete it
        if item_ingredient.mass == 0:
            item_ingredient.delete()
    for tag_name in tags:
        if not Tag.objects.filter(name=tag_name).exists():
            print("Tag does not exist, creating tag: " + str(tag_name))
            tag = Tag(name=tag_name)
            tag.save()
        #if the tag is not already associated with the item, add it
        tag = Tag.objects.get(name=tag_name)
        if not item.tags.filter(name=tag_name).exists():
            print("Tag is not already associated with item, adding tag: " + str(tag_name) + " to item: " + str(item.name))
            item.tags.add(tag)
            

    # modify the Item instance
    if name:
        item.name = name
    if description:
        item.description = description
    if price:
        item.price = price
    if link:
        item.link = link
    if servings:
        item.servings = servings
    item.save()
    
    return JsonResponse({"message": "Item updated successfully"})

@csrf_exempt
def get_current_table_data(request): #takes a list of selectedIngredients, an array of "conditions" strings, an array of "columns" strings, and returns the new table data
    #a condition may be "ingredient1>ingredient2" etc, "ingredient1>x" etc, "ingredient1=x", "ingredient1!x" 
    #a column may be "ingredient1/ingredient2", "ingredient1/x", "ingredient1/price", etc
    
    data = json.loads(request.body)
    selected_ingredients_data = data.get('selectedIngredients', [])
    selected_ingredient_ids = []
    selected_ingredients = []
    conditions = data.get('conditions', [])
    columns = data.get('columns', [])
    response = []
    item_count = 0
    max_items = 100
    
    if len(selected_ingredients_data) == 0:
        for item in Item.objects.all():
            item_data = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "Price": item.price,
                "link": item.link,
                "servings": item.servings
            }
            response.append(item_data)
        return JsonResponse(response, safe=False)
    
    for ingredient_data in selected_ingredients_data:
        ingredient_id = ingredient_data.get('id')
        ingredient = Ingredient.objects.get(id=ingredient_id)
        selected_ingredients.append(ingredient)
        selected_ingredient_ids.append(ingredient_id)
        
        
    filter_query = Q()
    for ingredient_id in selected_ingredient_ids:
        filter_query |= Q(itemingredient__ingredient__id=ingredient_id) # the |= operator is the same as the += operator for lists
    
    items = Item.objects.filter(filter_query).distinct()
    
    for item in items:
        itemMeetsAllConditions = True
        item_data = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "Price": item.price,
            "link": item.link,
            "servings": item.servings
        }
        
        item_ingredients = item.itemingredient_set.all().select_related('ingredient') # get all ItemIngredient instances associated with the item
        for ingredient in selected_ingredients:
            try:
                item_ingredient = next(item_ingredient for item_ingredient in item_ingredients if item_ingredient.ingredient == ingredient)
                ingredientMass = item_ingredient.mass
                item_data[ingredient.name] = ingredientMass
            except StopIteration:
                itemMeetsAllConditions = False
                break
            
        if not itemMeetsAllConditions:
            continue
            
        for condition in conditions:
            #finds the operator
            for char in condition:
                if char == ">" or char == "<" or char == "=" or char == "!":
                    operator = char
            var1, var2 = condition.split(operator)
            
            #if var1 contains a "/", then it is a column, so we need to find the value of the column
            #else, set var1Comparison to item_data[var1]
            if "/" in var1:
                part1, part2 = var1.split("/")
                var1Comparison = item_data[part1] / item_data[part2]
            else:
                var1Comparison = item_data[var1]
                
            try:
                var2Comparison = float(var2)
            except ValueError:
                var2Comparison = item_data[var2]
            
            
            # Perform comparisons
            if operator == ">" and not (var1Comparison > var2Comparison):
                itemMeetsAllConditions = False
                break
            elif operator == "<" and not (var1Comparison < var2Comparison):
                itemMeetsAllConditions = False
                break
            elif operator == "==" and not (var1Comparison == var2Comparison):
                itemMeetsAllConditions = False
                break
            elif operator == "!=" and not (var1Comparison != var2Comparison):
                itemMeetsAllConditions = False
                break
                
        if not itemMeetsAllConditions:
            continue
                
        for column in columns:
            var1, operator, var2 = column.partition("/")
            item_data[column] = item_data[var1] / item_data[var2]
        
                
        if itemMeetsAllConditions:
            response.append(item_data)
            item_count += 1
            # if item_count >= max_items:
            #     break
            
        
    # if item_count >= max_items: # if the number of items is greater than or equal to the max number of items, return the first max_items items
    #     print("item_count: " + str(item_count) + " is greater than or equal to max_items: " + str(max_items))
    #     return JsonResponse(response[:max_items], safe=False)
    return JsonResponse(response, safe=False)
        


@csrf_exempt
def delete_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()

    return JsonResponse({"message": "Item deleted successfully"})

@csrf_exempt
def create_ingredient(request):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    units = data.get('units', '') # optional

    ingredient = Ingredient(name=name, description=description, price=price, units=units)
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


def get_all_ingredients(request):
    ingredients = Ingredient.objects.all()
    response = []
    for ingredient in ingredients:
        response.append({
            "id": ingredient.id,
            "name": ingredient.name,
            "description": ingredient.description,
            "price": ingredient.price,
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