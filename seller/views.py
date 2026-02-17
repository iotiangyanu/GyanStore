from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from shop import models
from django.db.models import Prefetch
from shop.models import *
# Create your views here.

def seller(request):
    query=request.GET.get('q')
    products= Product.objects.select_related('category').all()
    context={
         'products':products
    }
    return render(request, 'seller.html',context)

def add_product(request):
    query = request.GET.get("q")
    category_slug=request.GET.get('category')
    categories = Category.objects.prefetch_related(
        Prefetch(
            "products"
        )
    )
    context={
         'categories':categories
         }
    if request.method =='POST':
            data=request.POST
            name=data.get('name')
            price=data.get('price')
            stock=data.get('stock')
            description=data.get('description')
            image=request.FILES.get('image')
            
            image_url=data.get('image_url')
            
            # Handle category - either selected or custom
            category_name = data.get('category')
            if category_name == 'custom':
                category_name = data.get('custom_category')
            
            # Create or get category
            if category_name:
                category_obj, created = Category.objects.get_or_create(name=category_name)
                
                # Create product
                product = Product(
                    name=name,
                    category=category_obj,
                    price=price,
                    stock=stock,
                    description=description,
                    image=image,
                    image_url=image_url
                )
                product.save()
                return redirect('seller')
            
    return render(request, 'add_product.html',context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        product.name = data.get('name')
        product.price = data.get('price')
        product.stock = data.get('stock')
        product.description = data.get('description')
        
        # Handle category
        category_id = data.get('category')
        if category_id:
            product.category = Category.objects.get(id=category_id)
        
        # Handle image upload
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        
        # Handle image URL
        if data.get('image_url'):
            product.image_url = data.get('image_url')
        
        product.save()
        return redirect('seller')
    
    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'edit_product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('seller')
    
    context = {'product': product}
    return render(request, 'delete_product.html', context)


        