from . import views
from django.urls import path, include
import seller
urlpatterns=[
    path('', views.login_view, name= 'login_page'),
    path('register/', views.register, name='register'),
    path('buyer-register/', views.buyer_register, name='buyer_register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
]