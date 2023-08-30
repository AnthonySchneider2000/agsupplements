import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Item
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# Create your views here.

def get_dummy_data(request):
    data = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'},
        {'id': 3, 'name': 'Item 3'},
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
def get_data(request):
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


# @api_view(['POST'])
# def create_item(request):
#     name = request.data.get('name')
#     description = request.data.get('description')
#     price = request.data.get('price')

#     item = Item(name=name, description=description, price=price)
#     item.save()

#     return Response({"message": "Item created successfully"})
