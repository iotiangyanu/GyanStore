from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/review/', views.add_review, name='add_review'),
]