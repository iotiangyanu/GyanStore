from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.urls import reverse
from .models import sellerProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                messages.error(request, 'Admin users must login through the admin panel.')
                return render(request, 'login.html')
            login(request, user)
            # Check if user is a seller (has sellerProfile)
            try:
                seller_profile = sellerProfile.objects.get(user=user)
                # User is a seller, redirect to seller dashboard
                return redirect('seller:seller')
            except sellerProfile.DoesNotExist:
                # User is a buyer, redirect to shop or next parameter
                next_url = request.POST.get('next') or request.GET.get('next') or 'shop_home'
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')
                
def register(request):
    if request.method == 'POST':
        # Handle form submission
        
        company_name=request.POST.get('company_name')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not all([company_name, first_name, last_name, username, password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'register.html')

        user=User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        sellerProfile.objects.create(user=user, company_name=company_name)
        return redirect('seller:seller')
        
def buyer_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not all([first_name, last_name, username, password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'buyer_register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'buyer_register.html')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'buyer_register.html')

    return render(request, 'register.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')