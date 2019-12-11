from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index ,name='index'),
    path('about_us',views.about_us,name='about_us'),
    path('logout',views.logout,name='logout'),
    path('principal_login',views.principal_login,name='principal_login'),
]