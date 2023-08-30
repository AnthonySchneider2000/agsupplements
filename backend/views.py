from django.shortcuts import render
from django.http import JsonResponse
from .models import Item
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# Create your views here.

def get_data(request):
    data = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'},
        {'id': 3, 'name': 'Item 3'},
    ]
    return JsonResponse(data, safe=False)


def create_item(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    price = request.POST.get('price')

    item = Item(name=name, description=description, price=price)
    item.save()

    return JsonResponse({"message": "Item created successfully"})



# @api_view(['POST'])
# def create_item(request):
#     name = request.data.get('name')
#     description = request.data.get('description')
#     price = request.data.get('price')

#     item = Item(name=name, description=description, price=price)
#     item.save()

#     return Response({"message": "Item created successfully"})
