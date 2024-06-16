from django.shortcuts import render, redirect, get_object_or_404
from shopapp.forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.http import require_POST
import time
from django.forms import modelformset_factory
import logging
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
import imaplib
import email
from email.policy import default
from django.shortcuts import render
from .models import Lead
import re
from django.contrib.auth.decorators import login_required



def generate_pdf(request, delivery_id):
    delivery = Delivery.objects.get(order_number=delivery_id)
    template_path = 'delivery_pdf_template.html'
    context = {'delivery': delivery}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="delivery_report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=settings.MEDIA_URL)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def get_customer_image(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        image_url = customer.profile_picture.url if customer.profile_picture else None
        return JsonResponse({'image_url': image_url})
    except Customer.DoesNotExist:
        return JsonResponse({})


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

@login_required(login_url='login')
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html',{})

@login_required(login_url='login')
def employee_dashboard(request):
    return render(request,'employee_dashboard.html')

@login_required(login_url='login')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

@login_required(login_url='login')
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

@login_required(login_url='login')
def admin_logout(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def customer_management(request):
    cust = Customer.objects.all()
    return render(request,'customer_mang.html',{'cust':cust})   

# Add Customer 👇👇
@login_required(login_url='login')
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

@login_required(login_url='login')
def emp_management(request):
    emp = Employee.objects.all()
    return render(request,'emp_management.html',{'emp':emp})    

@login_required(login_url='login')
def dealer_Management(request):
    d = Dealer.objects.all()
    return render(request,'dealer_mang.html',{'d':d})

@login_required(login_url='login')
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



@login_required(login_url='login')
def add_dealer1(request):
    if request.method == 'POST':
        d_form = DealerForm(request.POST)
        if d_form.is_valid():
            dealer = d_form.save()
            request.session['dealer_id'] = dealer.id  # Save dealer ID in session
            return redirect('dealer_management')  # Redirect to create_dealer view
    else:
        d_form = DealerForm()
    
    context = {
        'd_form': d_form,
    }
    return render(request, 'add_dealer1.html', context)

@login_required(login_url='login')
def create_dealer(request):
    if request.method == 'POST':
        form = TabletForm(request.POST)
        time.sleep(2)
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

@login_required(login_url='login')
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


@login_required(login_url='login')
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

@login_required(login_url='login')
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
                # tablet = sales_item.medicine
                # sales_item.price = tablet.price
                sales_item.save()
                return redirect('sale_mang')  
    else:
        form = SaleItemForm()
    
    return render(request, 'partials/sale_form.html', {'form': form})

@login_required(login_url='login')
def edit_sale(request, pk):
    sale = get_object_or_404(Sale, id=pk)
    sale_items = SaleItem.objects.filter(sale_id=sale.id)
    SaleFormSet = modelformset_factory(SaleItem, fields=('medicine', 'quantity'), extra=0)

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        formset = SaleFormSet(request.POST, queryset=sale_items)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            delivery, created = Delivery.objects.get_or_create(sale=sale, defaults={'status': 'pending'})

            if not created:
                
                delivery.status = 'updated'  
                delivery.save()

            return redirect('sale_mang')
    else:
        form = SaleForm(instance=sale)
        formset = SaleFormSet(queryset=sale_items)

    return render(request, 'edit_sale.html', {'form': form, 'sale': sale, 'formset': formset, 'sale_items': sale_items})

@login_required(login_url='login')
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

@login_required(login_url='login')
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        time.sleep(3)
        if form.is_valid():
            purchase_item = form.save(commit=False)
            purchase_id = request.session.get('purchase_id')
            print(purchase_id)
            tab = form.cleaned_data['tablet_name']
            print(tab)
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

@login_required(login_url='login')
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
    
@login_required(login_url='login')
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

@login_required(login_url='login')
def medicine_management(request):
    med = Medicine.objects.all()
    return render(request,'medicine_mang.html',{'med':med})

@login_required(login_url='login')
def add_medicine(request):
    tablets = Tablet.objects.all()
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
    return render(request, 'add_medicine.html', {'form': form,'tablets':tablets})

@login_required(login_url='login')
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

@login_required(login_url='login')
def sale_management(request):
    s = Sale.objects.all()
    return render(request,'sale_mang.html',{'s':s})  

@login_required(login_url='login')
def delete_sale(request,pk):
    res = Sale.objects.get(id=pk)
    res.delete()
    return redirect('sale_mang')

@login_required(login_url='login')
def purchase_management(request):
    purchases = Purchase.objects.prefetch_related('purchaseitem_set').all()
    for purchase in purchases:
        purchase.items = purchase.purchaseitem_set.all()
    return render(request, 'purchase_mang.html', {'pur': purchases})

@login_required(login_url='login')
def delete_purchase(request,pk):
    res = Purchase.objects.get(id=pk)
    res.delete()
    return redirect('purchase_mang')
    

@login_required(login_url='login')
def delete_dealer(request,pk):
    res = Dealer.objects.get(id=pk)
    res.delete()
    return redirect('dealer_management')

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_medicine(request,pk):
    res = Medicine.objects.get(id=pk)
    res.delete()
    return redirect('medicine_management')

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_employee(request,pk):
    res = Employee.objects.get(id=pk)
    res.delete()
    return redirect('emp_management')

# Add Customer 👇👇
# def add_customer(request):
#     cus=Customer.objects.all()
#     if request.method == 'POST':
#         form = CustomerForm(request.POST,request.FILES)

#         if form.is_valid():
#             customer = form.save(commit=False)
#             user = User.objects.create_user(username=customer.username,password = customer.password,first_name=customer.first_name,last_name=customer.last_name,email=customer.mail_id)
#             customer.user = user
#             customer.role = 'Customer'
#             customer.save()

#             UserDetails.objects.create(user=user,role='Customer')

#             return redirect('customer_management')
#     else:
#         form = CustomerForm()
#     return render(request, 'add_customer.html', {'form': form})

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_customer(request,pk):
    res = Customer.objects.get(id=pk)
    res.delete()
    return redirect('customer_management')

@login_required(login_url='login')
def delivery_management(request):
    dlry = Delivery.objects.all()
    return render(request,'delivery_mang.html',{'dlry':dlry})

@login_required(login_url='login')
def delivery_report(request,pk):
    dlry = Delivery.objects.get(id=pk)
    return render(request,'delivery_report.html',{'dlry':dlry})

@login_required(login_url='login')
def confirm(request):
    sales = Sale.objects.all()
    return render(request,'confirm.html',{'sales':sales})

@login_required(login_url='login')
def confirm_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.confirmed = 'SALE DELIVERY'
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


@login_required(login_url='login')
def crm_management(request):
    crm = Lead.objects.all()
    return render(request,'crm_mang.html',{'crm':crm})

@login_required(login_url='login')
def view_lead(request):
    le = Lead.objects.all()
    return render(request,'view_lead.html',{'le':le})

@login_required(login_url='login')
def confirm_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.status = True
        lead.save()
        return redirect('view_lead')
    return render(request, 'confirm_lead.html', {'lead': lead})
    
@login_required(login_url='login')
def view_opportunity(request):
    oppo = Opportunity.objects.all()
    return render(request,'view_opportunity.html',{'oppo':oppo})

@login_required(login_url='login')
def confirm_opportunity(request, pk):
    oppo = get_object_or_404(Opportunity, pk=pk)
    if request.method == 'POST':
        oppo.status = True
        oppo.save()
        return redirect('view_opportunity')
    return render(request, 'confirm_opportunity.html', {'oppo': oppo})    

@login_required(login_url='login')
def view_sale_order(request):
    sale_order = SalesOrder.objects.all()
    return render(request,'view_sale_order.html',{'sale_order':sale_order})

@login_required(login_url='login')
def extract_email_details(email_body):
    name = re.search(r"Name:\s*(.*)", email_body).group(1)
    phone = re.search(r"Phone:\s*(.*)", email_body).group(1)
    email_id = re.search(r"Email:\s*(.*)", email_body).group(1)
    tablet = re.search(r"Tablet:\s*(.*)", email_body).group(1)
    quantity = re.search(r"Quantity:\s*(.*)", email_body).group(1)
    price = re.search(r"Price:\s*(.*)", email_body).group(1)
    
    return {
        'name': name.strip(),
        'phone': int(phone.strip()),
        'email': email_id.strip(),
        'tablet': tablet.strip(),
        'quantity': int(quantity.strip()),
        'price': float(price.strip())
    }

def fetch_and_store_email_data(request):
    # Connect to the email server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login("activecustomer.email@gmail.com", "mdti hyxy cpzp iozr")
    mail.select('inbox')

    # Search for unseen emails
    status, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    for email_id in email_ids:
        # Fetch the email
        status, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]

        # Parse the email content
        msg = email.message_from_bytes(raw_email, policy=default)
        email_body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_body = part.get_payload(decode=True).decode()
                    break
        else:
            email_body = msg.get_payload(decode=True).decode()

        # Extract details from the email body
        details = extract_email_details(email_body)

        # Store the details in the Lead model
        Lead.objects.create(
            name=details['name'],
            phone=details['phone'],
            email=details['email'],
            tablet=details['tablet'],
            quantity=details['quantity'],
            price=details['price']
        )
    return redirect('crm_mang')