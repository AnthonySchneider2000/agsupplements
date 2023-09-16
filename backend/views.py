import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Item, Ingredient, ItemWithIngredients, ItemIngredient
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
def create_item(request):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    item = Item(name=name, description=description, price=price)
    item.save()

    return JsonResponse({"message": "Item created successfully"})

@csrf_exempt
def delete_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()

    return JsonResponse({"message": "Item deleted successfully"})

# get data from database
def get_item(request):
    items = Item.objects.all()
    response = []
    for item in items:
        response.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price
        })
    return JsonResponse(response, safe=False)

@csrf_exempt
def create_item_with_ingredients(request):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    ingredient_data = data.get('ingredients', [])

    # Create the ItemWithIngredients instance
    item = ItemWithIngredients(name=name, description=description, price=price)
    item.save()

    # Create ItemIngredient instances for each ingredient and associate them with the item
    for ingredient_info in ingredient_data:
        ingredient_id = ingredient_info.get('ingredient_id')
        mass = ingredient_info.get('mass')

        ingredient = Ingredient.objects.get(id=ingredient_id)
        item_ingredient = ItemIngredient(item=item, ingredient=ingredient, mass=mass)
        item_ingredient.save()

    return JsonResponse({"message": "Item with ingredients created successfully"})

def get_item_with_ingredients(request, id):
    try:
        item = ItemWithIngredients.objects.get(id=id)
    except ItemWithIngredients.DoesNotExist:
        return JsonResponse({"message": "Item with ingredients not found"}, status=404)

    # Retrieve the ingredients and their masses associated with the item
    ingredients = item.ingredients.all()
    ingredient_data = [{'ingredient_id': ingredient.id, 'name': ingredient.name, 'mass': item_ingredient.mass}
                      for ingredient, item_ingredient in zip(ingredients, item.itemingredient_set.all())]

    response = {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "ingredients": ingredient_data
    }

    return JsonResponse(response)

def delete_item_with_ingredients(request, id):
    item = ItemWithIngredients.objects.get(id=id)
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
