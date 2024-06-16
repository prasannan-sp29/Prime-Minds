from django.shortcuts import render, redirect, get_object_or_404
from shopapp.forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.http import require_POST
import time
from django.forms import modelformset_factory

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
    if request.method == 'POST':
        d_form = DealerForm(request.POST)
        form = TabletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dealer_management')
    else:
        d_form = DealerForm()
        form = TabletForm()
    return render(request,'index.html',{'d_form':d_form,'form':form})











def index1(request):
    context = {
        'form':ContactForm()
    }
    return render(request,'index1.html',context)

def create_contace(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request,'partials/form2.html',{'form':ContactForm()})


pk1 = 0
def add_dealer1(request):
    if request.method == 'POST':
        d_form = DealerForm(request.POST)
        if d_form.is_valid():
            dealer = d_form.save()
            request.session['dealer_id'] = dealer.id  # Save dealer ID in session
            # return redirect('create-dealer')  # Redirect to create_dealer view
    else:
        d_form = DealerForm()
    
    context = {
        'd_form': d_form,
    }
    return render(request, 'add_dealer1.html', context)

def create_dealer(request):
    if request.method == 'POST':
        form = TabletForm(request.POST)
        time.sleep(3)
        if form.is_valid():
            tablet = form.save(commit=False)
            dealer_id = request.session.get('dealer_id')  
            dealer = Dealer.objects.get(pk=dealer_id)
            tablet.dealer = dealer  
            tablet.save()
            return redirect('dealer_management')
    else:
        form = TabletForm()
    
    context = {
        'form': form,
    }
    return render(request, 'partials/form.html', context)

def edit_dealer(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    TabletFormSet = modelformset_factory(Tablet, fields=('tablet_name', 'price'), extra=0)
    
    if request.method == 'POST':
        form = DealerForm(request.POST, instance=dealer)
        formset = TabletFormSet(request.POST, queryset=Tablet.objects.filter(dealer_id=dealer.id))
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dealer_management')
    else:
        form = DealerForm(instance=dealer)
        formset = TabletFormSet(queryset=Tablet.objects.filter(dealer_id=dealer.id))
    
    return render(request, 'edit_dealer.html', {'form': form, 'formset': formset, 'dealer': dealer})



def new_sale(request):
    if request.method == 'POST':
        s_form = SaleForm(request.POST)
        if s_form.is_valid():
            sale = s_form.save()
            request.session['sale_id'] = sale.id  
            return redirect('sale_mang')  
    else:
        s_form = SaleForm()
    
    return render(request, 'new_sale.html', {'s_form': s_form})

def create_sale(request):
    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        time.sleep(3)
        if form.is_valid():
            sales_item = form.save(commit=False)
            sale_id = request.session.get('sale_id')
            if sale_id:
                sale = Sale.objects.get(pk=sale_id)
                sales_item.sale = sale
                tablet = sales_item.medicine
                sales_item.price = tablet.price
                sales_item.save()
                return redirect('sale_mang')  
    else:
        form = SaleItemForm()
    
    return render(request, 'partials/sale_form.html', {'form': form})

def edit_sale(request,pk):
    res = Sale.objects.get(id=pk)
    res1 = SaleItem.objects.filter(id=res.id)
    customer = get_object_or_404(Sale,pk=pk)
    SaleFormSet = modelformset_factory(SaleItem,fields=('medicine','quantity'),extra=0)
    if request.method == 'POST':
        form = SaleForm(request.POST,instance=customer)
        formset = SaleFormSet(request.POST,queryset=SaleItem.objects.filter(sale_id = customer.id))
        if form.is_valid():
            form.save()
            formset.save()
            return redirect('sale_mang')
    else:
        form = SaleForm(instance=customer)
        formset = SaleFormSet(queryset=SaleItem.objects.filter(sale_id=customer.id))
    return render(request,'edit_sale.html',{'form':form,'res':res,'customer':customer,'formset':formset,'res1':res1})

def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()
            request.session['purchase_id'] = purchase.id 
            return redirect('purchase_mang')  
    else:
        form = PurchaseForm()
    return render(request, 'new_purchase.html', {'form': form})

def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        time.sleep(3)
        if form.is_valid():
            purchase_item = form.save(commit=False)
            purchase_id = request.session.get('purchase_id')
            print(purchase_id)
            if purchase_id:
                
                purchase = Purchase.objects.get(pk=purchase_id)
                purchase_item.purchase = purchase
                purchase_item.save()
                return redirect('purchase_mang')
        else:
            print("Not Valid")
            print(form.errors)
    else:
        form = PurchaseItemForm()
    return render(request, 'partials/purchase_form.html', {'form': form})


def edit_purchase(request,pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    PurchaseFormSet = modelformset_factory(PurchaseItem, fields=('tablet_name', 'price','quantity'), extra=0)
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseFormSet(request.POST, queryset=PurchaseItem.objects.filter(purchase_id=purchase.id))
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('purchase_mang')
    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseFormSet(queryset=PurchaseItem.objects.filter(purchase_id=purchase.id))
    
    return render(request, 'edit_purchase.html', {'form': form, 'formset': formset, 'purchase': purchase})


















def add_dealer(request):
    if request.method == 'POST':
        t_form = TabletForm(request.POST)
        d_form = DealerForm(request.POST)
        if d_form.is_valid() and t_form.is_valid():
            d = d_form.save()
            t = t_form.save(commit=False)
            t.dealer = d
            t.save()

            return redirect('dealer_management')
    else:
        t_form = TabletForm()
        d_form = DealerForm()
    
    return render(request, 'add_dealer.html', {'d_form': d_form,'t_form':t_form})

def medicine_management(request):
    med = Medicine.objects.all()
    return render(request,'medicine_mang.html',{'med':med})

def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            try:
                med = form.save(commit=False)
                tablet = med.medicine_name
                med.price = tablet.price
                med.save()
                return redirect('medicine_management')
            except IntegrityError:
                form.add_error(None, 'There was an error saving the medicine. Please try again.')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})



def sale_management(request):
    s = Sale.objects.all()
    return render(request,'sale_mang.html',{'s':s})  


def delete_sale(request,pk):
    res = Sale.objects.get(id=pk)
    res.delete()
    return redirect('sale_mang')

def purchase_management(request):
    purchases = Purchase.objects.prefetch_related('purchaseitem_set').all()
    for purchase in purchases:
        purchase.items = purchase.purchaseitem_set.all()
    return render(request, 'purchase_mang.html', {'pur': purchases})

def delete_purchase(request,pk):
    res = Purchase.objects.get(id=pk)
    res.delete()
    return redirect('purchase_mang')
    


def delete_dealer(request,pk):
    res = Dealer.objects.get(id=pk)
    res.delete()
    return redirect('dealer_management')


def edit_medicine(request,pk):
    if request.method == 'POST':
        res = Medicine.objects.get(id=pk)
        form = MedicineForm(request.POST,instance=res)
        if form.is_valid():
            try:
                med = form.save(commit=False)
                tablet = med.medicine_name
                med.price = tablet.price
                med.save()
                return redirect('medicine_management')
            except IntegrityError:
                form.add_error(None, 'There was an error saving the medicine. Please try again.')
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
        return redirect('sale_mang')
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