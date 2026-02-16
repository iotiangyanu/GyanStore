from . import views
from django.urls import path, include

urlpatterns=[
    path('', views.login_page, name= 'login_page'),
]