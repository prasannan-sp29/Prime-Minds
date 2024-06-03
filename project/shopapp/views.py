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
    return render(request, 'add_customer.html', {'form': form})

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

def customer_management(request):
    return render(request,'customer_mang.html')   

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

# Add Customer 👇👇
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES)

        if form.is_valid():
            customer = form.save(commit=False)
            user = User.objects.create_user(username=customer.username,password = customer.password,first_name=customer.first_name,last_name=customer.last_name,email=customer.mail_id)
            customer.user = user
            customer.role = 'Customer'
            customer.save()

            UserDetails.objects.create(user=user,role='Customer')

            # return redirect('view_customers')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

def view_customers(request):
    customers = Customer.objects.all()
    return render(request, 'shop/view_customers.html', {'customers': customers})     

def employee_dashboard(request):
    return render(request,'employee_dashboard.html')

def emp_management(request):
    return render(request,'emp_management.html')    

def view_employees(request):
    employees = Employee.objects.all()
    return render(request, 'shop/view_employees.html', {'employees': employees})

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

def dealer_Management(request):
    deal = Dealer.objects.all()
    return render(request,'dealer_mang.html',{'deal':deal})

def add_dealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dealer_management')
    else:
        form = DealerForm()
    return render(request, 'add_dealer.html', {'form': form})

def view_dealers(request):
    dealers = Dealer.objects.all()
    return render(request, 'view_dealers.html', {'dealers': dealers})

def medicine_management(request):
    return render(request,'medicine_mang.html')

def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_medicines')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

def view_medicines(request):
    medicines = Medicine.objects.all()
    return render(request, 'view_medicines.html', {'medicines': medicines})  

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

def Sale(request):
    if request.method == 'POST':
        user_form = userForm(request.POST)
        sale_form = SaleForm(request.POST)
        if user_form.is_valid() and sale_form.is_valid():
            customer = user_form.save()
            purchase = sale_form.save(commit=False)
            purchase.customer = customer
            purchase.save()
            return redirect('success')
    else:
        user_form = userForm()
        sale_form = SaleForm()
    
    return render(request, 'new_sale.html', {'user_form': user_form, 'sale_form': sale_form})

def sale_management(request):
    return render(request,'sale_mang.html')  

def purchase_management(request):
    return render(request,'purchase_mang.html')

def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page after saving
    else:
        form = PurchaseForm()
    return render(request, 'new_purchase.html', {'form': form})