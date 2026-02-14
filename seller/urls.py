from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller_home, name='seller_home'),
    path('dashboard/', views.seller_home, name='seller_home'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/', views.add_product, name='edit_product'),
    
]