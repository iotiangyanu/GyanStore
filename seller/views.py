from django.shortcuts import render
from django.http import HttpResponse
from shop import models
# Create your views here.

def seller(request):
    return render(request, 'seller.html')

def add_product(request):
    return render(request, 'add_product.html')

def edit_product(request):
    return render(request, 'edit_product.html')