from django.shortcuts import render, redirect
from shopapp.forms import userForm
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *

def register(request):
    if request.method == "POST":
        form = userForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            C = Customer(first_name = first_name,last_name=last_name,mail_id=email,role='Customer')
            C.save()
            form.save()
            return redirect('login')  
    else:
        form = userForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user) 
                return redirect('customer_dashboard')
            else:
                return HttpResponse('User is not active')
        else:
            return HttpResponse('Please check your credentials')
    return render(request, "login.html", {})

def customer_dashboard(request):
    data = userdetials.objects.all()
    return render(request, 'customer_dashboard.html',{'data':data})
