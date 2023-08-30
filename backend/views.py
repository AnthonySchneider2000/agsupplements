from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def get_data(request):
    data = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'},
        {'id': 3, 'name': 'Item 3'},
    ]
    return JsonResponse(data, safe=False)
