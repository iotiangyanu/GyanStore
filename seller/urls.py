from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller, name='seller'),
    path('seller/', views.seller, name='seller'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/', views.edit_product, name='edit_product'),
    
]