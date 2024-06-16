from django.shortcuts import render, redirect, get_object_or_404
from shopapp.forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.http import require_POST

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

            return redirect("emp_management")
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

def customer_management(request):
    cust = Customer.objects.all()
    return render(request,'customer_mang.html',{'cust':cust})   

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

            return redirect('customer_management')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

def emp_management(request):
    emp = Employee.objects.all()
    return render(request,'emp_management.html',{'emp':emp})    


def dealer_Management(request):
    deal = Dealer.objects.all()
    return render(request,'dealer_mang.html',{'deal':deal})

def index(request):
    form = TabletForm()
    return render(request,'index.html',{'form':form})

def add_dealer(request):
    if request.method == 'POST':
        # dealer_form = DealerForm(request.POST)
        tablet_formset = TabletForm(request.POST)
        print('HHHHHHHHHHHHHHiiiiiiiiiiiiiiiiiii')
        if tablet_formset.is_valid():
            # dealer = dealer_form.save()
            tablet_formset.save()
            print("data saved successfully")
           
            return redirect('dealer_management')
    else:
        # dealer_form = DealerForm() 
        tablet_formset = TabletForm()
    return render(request, 'partials/tablet_form.html', {'form': tablet_formset})

def medicine_management(request):
    med = Medicine.objects.all()
    return render(request,'medicine_mang.html',{'med':med})

def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_management')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})


def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

def new_sale(request):
    if request.method == 'POST':
        
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale_form.save()
            return redirect('sale_mang')
    else:
        
        sale_form = SaleForm()
    
    return render(request, 'new_sale.html', {'sale_form': sale_form})

def sale_management(request):
    s = Sale.objects.all()
    return render(request,'sale_mang.html',{'s':s})  

def edit_sale(request,pk):
    if request.method == 'POST':
        res = Sale.objects.get(id=pk)
        form = SaleForm(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('sale_mang')
    else:
        res = Sale.objects.get(id=pk)
        form = SaleForm(instance=res)
    return render(request,'edit_sale.html',{'form':form,'res':res})

def delete_sale(request,pk):
    res = Sale.objects.get(id=pk)
    res.delete()
    return redirect('sale_mang')

def purchase_management(request):
    pur = Purchase.objects.all()
    return render(request,'purchase_mang.html',{'pur':pur})

def create_purchase(request):

    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST)
        if purchase_form.is_valid() and formset.is_valid():
            purchase = purchase_form.save(commit=False)
            purchase.save()
            items = formset.save(commit=False)
            for item in items:
                item.purchase = purchase
                item.save()
            formset.save_m2m()
            return redirect('purchase_mang')
    else:
        purchase_form = PurchaseForm()
        formset = PurchaseItemFormSet()


    return render(request, 'new_purchase.html', {'purchase_form': purchase_form,'formset': formset,})

def edit_purchase(request,pk):
    if request.method == 'POST':
        res = Purchase.objects.get(id=pk)
        form = PurchaseForm(request.POST,request.FILES,instance=res)
        if form.is_valid():
            form.save()
            return redirect('purchase_mang')
    else:
        res = Purchase.objects.get(id=pk)
        form = PurchaseForm(instance=res)
    return render(request,'edit_purchase.html',{'form':form,'res':res})

def delete_purchase(request,pk):
    res = Purchase.objects.get(id=pk)
    res.delete()
    return redirect('purchase_mang')
    
# dfghjkkkkkkkkkkkkkkk
def edit_dealer(request,pk):
    res = Dealer.objects.get(id=pk)
    res1 = Tablet.objects.filter(dealer_id=res.id)
    if request.method == 'POST':
        dealer_form = DealerForm(request.POST,instance=res)
        tablet_formset = TabletFormSet(request.POST,instance=res1)
        if dealer_form.is_valid() and tablet_formset.is_valid():
            dealer = dealer_form.save()
            for form in tablet_formset:
                tablet = form.save(commit=False)
                tablet.dealer = dealer
                tablet.save()
            return redirect('dealer_management')
    else:
        dealer_form = DealerForm(instance=res)
        tablet_formset = TabletFormSet(instance=res1)
    return render(request,'edit_dealer.html',{'dealer_form': dealer_form, 'tablet_formset': tablet_formset})

def delete_dealer(request,pk):
    res = Dealer.objects.get(id=pk)
    res.delete()
    return redirect('dealer_management')


def edit_medicine(request,pk):
    if request.method == 'POST':
        res = Medicine.objects.get(id=pk)
        form = MedicineForm(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('medicine_management')

    else:
        res = Medicine.objects.get(id=pk)
        form = MedicineForm(instance=res)
    return render(request,'edit_medicine.html',{'form':form,'res':res})

def delete_medicine(request,pk):
    res = Medicine.objects.get(id=pk)
    res.delete()
    return redirect('medicine_management')

def edit_employee(request,pk):
    if request.method == 'POST':
        res = Employee.objects.get(id=pk)
        form = EmployeeForm(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('emp_management')

    else:
        res = Employee.objects.get(id=pk)
        form = EmployeeForm(instance=res)
    return render(request,'edit_employee.html',{'form':form,'res':res})

def delete_employee(request,pk):
    res = Employee.objects.get(id=pk)
    res.delete()
    return redirect('emp_management')

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

            return redirect('customer_management')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

def edit_customer(request,pk):
    if request.method == 'POST':
        res = Customer.objects.get(id=pk)
        form = CustomerForm1(request.POST,request.FILES,instance=res)
        if form.is_valid():
            form.save()
            return redirect('customer_management')
    else:
        res = Customer.objects.get(id=pk)
        form = CustomerForm1(instance=res)
    return render(request,'edit_customer.html',{'form':form,'res':res})

def delete_customer(request,pk):
    res = Customer.objects.get(id=pk)
    res.delete()
    return redirect('customer_management')


def delivery_management(request):
    dlry = Delivery.objects.all()
    return render(request,'delivery_mang.html',{'dlry':dlry})

def confirm(request):
    sales = Sale.objects.all()
    return render(request,'confirm.html',{'sales':sales})

def confirm_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.confirmed = True
        sale.save()
        return redirect('confirm')
    return render(request, 'confirm_sale.html', {'sale': sale})

@require_POST
def change_status(request):
    delivery_id = request.POST.get('delivery_id')
    new_status = request.POST.get('status')
    try:
        delivery = Delivery.objects.get(pk=delivery_id)
        delivery.status = new_status
        delivery.save()
    except Delivery.DoesNotExist:
        print('delivery model doesnotexist')

    return redirect('delivery_mang')

def delivery_report(request,pk):
    dlry = Delivery.objects.get(id=pk)
    return render(request,'delivery_report.html',{'dlry':dlry})

def crm_management(request):
    crm = Lead.objects.all()
    return render(request,'crm_mang.html',{'crm':crm})

def view_lead(request):
    le = Lead.objects.all()
    return render(request,'view_lead.html',{'le':le})

def confirm_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.status = True
        lead.save()
        return redirect('view_lead')
    return render(request, 'confirm_lead.html', {'lead': lead})



def view_opportunity(request):
    oppo = Opportunity.objects.all()
    return render(request,'view_opportunity.html',{'oppo':oppo})

def confirm_opportunity(request, pk):
    oppo = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        oppo.status = True
        oppo.save()
        return redirect('view_opportunity')
    return render(request, 'confirm_opportunity.html', {'oppo': oppo})    

def view_sale_order(request):
    sale_order = SalesOrder.objects.all()
    return render(request,'view_sale_order.html',{'sale_order':sale_order})