from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
# from . models import gfm_signup
import psycopg2

numalpha='abcdefghijklmnopqrstuvwxyz0123456789'
key=5


# Create your views here.
def index(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    else:
        auth.logout(request)
        return redirect('/')

#************************************************************************************************************************************

def about_us(request):
    if request.method == 'POST':
        return render(request,'about_us.html') 
    else:
        return render(request,'about_us.html')

#************************************************************************************************************************************


def principal_login(request):
    return render(request,'principal_login.html')




#************************************************************************************************************************************

#************************************************************************************************************************************
def logout(request):
    auth.logout(request)
    return redirect('/')