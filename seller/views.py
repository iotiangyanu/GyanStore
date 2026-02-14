from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def seller_home(request):
    return render(request, 'dashboard.html')

def add_product(request):
    return render(request, 'add_product.html')

def edit_product(request):
    return render(request, 'edit_product.html')