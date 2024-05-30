from django.shortcuts import render, redirect
from shopapp.forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *

def register(request):
    if request.method == "POST":
        form = userForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            username = user.username
            password = form.cleaned_data.get('password') 
            user.set_password(password)
            user.save()

            UserDetails.objects.create(user=user,role='Customer')
            
            Customer.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                mail_id=user.email,   
            )

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
                rle = UserDetails.objects.get(user=user)
                # print(rle.role)
                if str(rle.role) == 'Customer':
                    return redirect('customer_dashboard')
                elif str(rle.role) == 'Employee':
                    return redirect('employee_dashboard')
                elif str(rle.role) == 'Admin':
                # else:
                    return redirect('admin_dashboard')
                
            else:
                return HttpResponse('User is not active')
        else:
            return HttpResponse('Please check your credentials')
    return render(request, "login.html", {})

def customer_dashboard(request):
    return render(request, 'customer_dashboard.html',{})

def employee_dashboard(request):
    return render(request,'employee_dashboard.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def add_employee(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            first_name = employee.first_name
            last_name = employee.last_name
            # role = employee.role
            email = employee.mail_id
            password = username[:4] + str(employee.phone_number)[-4:]
            # create user
            user = User.objects.create_user(
                username=username, email=email, password=password,first_name=first_name,last_name=last_name
            )

            employee.user = user
            employee.id = user.id
            employee.save()

            # create user details
            UserDetails.objects.create(user=user,role = 'Employee')

            return redirect("admin_dashboard")
    else:
        form = EmployeeForm()
    
    return render(request,'add_employee.html',{'form':form})

def add_admin(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        form = EmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            first_name = employee.first_name
            last_name = employee.last_name
            # role = employee.role
            email = employee.mail_id
            password = username[:4] + str(employee.phone_number)[-4:]
            # create user
            user = User.objects.create_user(
                username=username, email=email, password=password,first_name=first_name,last_name=last_name
            )

            employee.user = user
            employee.id = user.id
            employee.save()

            # create user details
            UserDetails.objects.create(user=user,role = 'Admin')

            return redirect("admin_dashboard")
    else:
        form = EmployeeForm()
    
    return render(request,'add_admin.html',{'form':form})

def dealer_management(request):
    return render(request,"dealer_management.html")