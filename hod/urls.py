from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index ,name='index'),
    path('about_us',views.about_us,name='about_us'),
    path('logout',views.logout,name='logout'),
    path('hod_login',views.hod_login,name='hod_login'),
    path('hod_accept',views.hod_accept,name='hod_accept'),
    path('hod_home',views.hod_home,name='hod_home'),
    path('hod_validate_gfm',views.hod_validate_gfm,name='hod_validate_gfm'),
    path('stu_report',views.stu_report,name='stu_report'),
    path('forget_pass1',views.forget_pass1,name='forget_pass1'),
    path('forget_pass2',views.forget_pass2,name='forget_pass2')
]
