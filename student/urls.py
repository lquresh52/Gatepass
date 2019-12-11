from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns=[
    path('index', views.index ,name='index'),
    path('about_us',views.about_us,name='about_us'),
    path('student_login',views.student_login,name='student_login'),
    path('signup_form',views.signup_form,name='signup_form'),
    path('forget_pass1',views.forget_pass1,name='forget_pass1'),
    path('forget_pass2',views.forget_pass2,name='forget_pass2'),
    path('stu_home',views.stu_home,name='stu_home'),
    path('logout',views.logout,name='logout'),
    path('in_apply',views.in_apply,name='in_apply'),
    path('out_apply',views.out_apply,name='out_apply'),
    path('inout_apply',views.inout_apply,name='inout_apply'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)