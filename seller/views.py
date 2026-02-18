from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from shop import models
from django.db.models import Prefetch
from shop.models import *
from accounts import urls
from accounts.models import sellerProfile

# Create your views here.

@login_required
def seller(request):
    try:
        profile = request.user.sellerprofile
        products = Product.objects.filter(seller=request.user)
        return render(request, 'seller.html', {'profile': profile, 'products': products})
    except sellerProfile.DoesNotExist:
        return redirect('register')  
    

def register(request):
    return render(request, 'registartion.html')   

@login_required
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
                    image_url=image_url,
                    seller=request.user
                )
                product.save()
                return redirect('seller:seller')
            
    return render(request, 'add_product.html',context)

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.seller != request.user:
        return redirect('seller:seller')
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        product.name = data.get('name')
        product.price = data.get('price')
        product.stock = data.get('stock')
        product.description = data.get('description')
        
        # Handle category - either selected or custom
        category_name = data.get('category')
        if category_name == 'custom':
            category_name = data.get('custom_category')
        
        if category_name:
            category_obj, created = Category.objects.get_or_create(name=category_name)
            product.category = category_obj
        
        # Handle image upload
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        
        # Handle image URL
        if data.get('image_url'):
            product.image_url = data.get('image_url')
        
        product.save()
        return redirect('seller:seller')
    
    context = {
        'product': product,
        'categories': categories
    }
    return render(request, 'edit_product.html', context)


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.seller != request.user:
        return redirect('seller:seller')
    
    if request.method == 'POST':
        product.delete()
        return redirect('seller:seller')
    
    context = {'product': product}
    return render(request, 'delete_product.html', context)


        