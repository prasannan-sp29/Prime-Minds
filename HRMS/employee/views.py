from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import userdetials
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from employee.models import Employee_data, Payroll, Attendance, Leave
from employee.forms import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_date
import pytz
import calendar
from datetime import datetime, timedelta
from datetime import datetime
import numpy as np
from .utils import *

# To Find Durations Between Two Dates
def get_leave_duration(start, end):
    return (end - start).days

@login_required(login_url='index')
def dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required(login_url='index')
def employeeDetails(request):
    data = Employee_data.objects.all()
    return render(request, "employee_details.html", {"data": data})

@login_required(login_url='index')
def know_more(request, pk):
    data = Employee_data.objects.get(id=pk)
    return render(request, "know_more.html", {"data": data})

@login_required(login_url='index')
def know_mores(request, pk):
    data = Employee_data.objects.get(id=pk)
    return render(request, "know_mores.html", {"data": data})

def remove_space(inp_str):
    return inp_str.replace(" ", "").lower()

@login_required(login_url='index')
def add_employee(request):
    if request.method == "POST":
        form = add_employee_form(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            username = remove_space(employee.name)
            email = employee.mail_id
            password = username[:4] + str(employee.phone_number)[-4:]
            
            # create user
            user = User.objects.create_user(username=username, email=email, password=password)
            employee.user = user
            employee.id = user.id
            employee.save()
            
            # create user details
            userdetials.objects.create(user=user)
            
            return redirect("employee_details")
    else:
        form = add_employee_form()
    return render(request, "add_employee.html", {"form": form})

@login_required(login_url='index')
def edit_profile(request, pk):
    data = Employee_data.objects.get(id=pk)
    if request.method == "POST":
        form = add_employee_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect("know_more", pk=pk)
    else:
        form = add_employee_form(instance=data)
    return render(request, "edit_profile.html", {"form": form})

def get_employee(request):
    return Employee_data.objects.get(user=request.user)

def get_employee_id(request):
    return get_employee(request).id

@login_required(login_url='index')
def generate_payslip(request):
    pay = Payroll.objects.all().order_by('-id')
    employees = Employee_data.objects.all()
    if request.method == "POST":
        form = PayrollForm(request.POST)
        employee_id = request.POST.get("employee_id")
        
        if form.is_valid():
            MONTH = form.cleaned_data["month"]
            # print('payslip for the month is --> ',MONTH)
            date_obj = datetime.strptime(str(MONTH), '%Y-%m-%d')
            # print(date_obj.month)
            mon = date_obj.month
            yr = date_obj.year

            if employee_id:
                employee = Employee_data.objects.get(id=employee_id)
                generate_single_payslip(employee, MONTH,mon,yr)
                messages.success(request, f"Payroll Generated Successfully for {employee.name}.")
            else:
                for i in employees:
                    generate_single_payslip(i, MONTH,mon,yr)
                messages.success(request, "Payroll Generated Successfully for all Employees.")
            
            return redirect('generate_payslip')
    else:
        form = PayrollForm()
    return render(request, "generate_payslip.html", {"form": form, "pay": pay, "employees": employees})

def generate_single_payslip(employee, month,mon,yr):
    ctc = employee.salary
    basic = (ctc * 0.40) / 12
    HRA = (basic * 0.50) / 12
    DA = (basic * 0.25) / 12
    TA = (basic * 0.10) / 12
    PF = (basic * 0.12) / 12
    PT = 200
    Gross_salary = basic + HRA + DA + TA
    IT = 0
    if Gross_salary > 200000:
        IT = Gross_salary * 0.10
    Total_gross1 = Gross_salary - (PF + IT + PT)

    # ------------------------- #
    last_day = calendar.monthrange(yr, mon)[1]
    end_of_month = datetime(yr, mon, last_day).date()
    start_date = datetime.combine(month, datetime.min.time())
    end_date = datetime.combine(end_of_month, datetime.min.time())
    total_days = ((end_date - start_date).days) + 1
    # print(total_days)
    days = np.busday_count(start_date.date(), end_date.date())

    total_working_days = days + 1
    # print(total_working_days)
    
    leave_days = total_days - total_working_days
    # print(leave_days)
    leaves_taken = 0
    start_ = timezone.datetime(yr, mon, 1)
    end_ = timezone.datetime(yr, mon + 1, 1) - timezone.timedelta(days=1)
    leaves = Leave.objects.filter(user_id = employee.id, status = 'Approved', startdate__lte=end_, enddate__gte=start_)
    # print(leaves)

    for i in leaves:
        leaves_taken += i.days
    
    present_days = total_working_days - leaves_taken
    
    # print('Leaves Taken --> ',leaves_taken)
    ###########################

    # per day salary
    per_day_salary = Total_gross1 / total_working_days
    # print('per day income --> ',per_day_salary)

    leave_deduction = per_day_salary * leaves_taken

    Total_gross = Total_gross1 - leave_deduction

    Payroll.objects.create(
        employee=employee,
        month=month,
        basic=basic,
        hra=HRA,
        da=DA,
        ta=TA,
        pf=PF,
        income_tax=IT,
        leave_deduction = leave_deduction,
        professional_tax=PT,
        gross=Gross_salary,
        total_gross=Total_gross,
    )

@login_required(login_url='index')
def generate_payslip_pdf(request, pk):
    slip = get_object_or_404(Payroll, id=pk)
    end_of_month = slip.get_end_of_month()
    # getMonth = slip.get_month()
    start = slip.month
    # print(getMonth)
    # Convert to datetime objects
    start_date = datetime.combine(start, datetime.min.time())
    end_date = datetime.combine(end_of_month, datetime.min.time())
    total_days = ((end_date - start_date).days) + 1
    # print(total_days)
    # print(total_days)
    # Calculate the number of business days
    days = np.busday_count(start_date.date(), end_date.date())

    total_working_days = days + 1
    
    leave_days = total_days - total_working_days
    # print(total_working_days)

    
    # ----------------------------- #
    leaves_taken = 0
    year = slip.get_year()
    month = slip.get_month()
    start_ = timezone.datetime(year, month, 1)
    end_ = timezone.datetime(year, month + 1, 1) - timezone.timedelta(days=1)
    leaves = Leave.objects.filter(user_id = slip.employee_id, status = 'Approved', startdate__lte=end_, enddate__gte=start_)
    # print(leaves)

    for i in leaves:
        leaves_taken += i.days
    
    present_days = total_working_days - leaves_taken

    return render(request, "payslip_template.html", {'leave_days':leave_days,"slip": slip, 'end_of_month': end_of_month, 'total_working_days': total_working_days,'leaves_taken':leaves_taken,'present_days':present_days})


def attendacne_view(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        action = request.POST.get("action")

        try:
            user1 = User.objects.get(username=user_name)
            user = Employee_data.objects.get(user_id=user1.id)
        except (User.DoesNotExist, Employee_data.DoesNotExist):
            return JsonResponse({"message": "User not found."}, safe=False)

        today = timezone.now().date()
        ist = pytz.timezone("Asia/Kolkata")

        attendance, created = Attendance.objects.get_or_create(user=user, date=today)

        if action == "log-in" and attendance.check_in_time is None:
            attendance.check_in_time = timezone.now().astimezone(ist).time()
            attendance.save()
            return JsonResponse({"message": "Log-in successful."}, safe=False)

        elif action == "log-out" and attendance.check_out_time is None:
            if attendance.check_in_time != None:
                attendance.check_out_time = timezone.now().astimezone(ist).time()
                attendance.save()
            else:
                return JsonResponse({'message':"You have not Loged In yet, First Login then Logout"})
            return JsonResponse({"message": "Log-out successful."}, safe=False)

        return JsonResponse({"message": "Action already recorded or invalid."}, safe=False)

    return render(request, "attendance.html")

@login_required(login_url='index')
def deleteEmployee(request, pk):
    res = get_object_or_404(Employee_data, id=pk)
    del_user = get_object_or_404(User, id=pk)
    u = get_object_or_404(userdetials, user_id=pk)
    del_user.delete()
    u.delete()
    res.delete()
    return redirect("employee_details")

@login_required(login_url='index')
def checkAttendance(request, pk):
    attend = Attendance.objects.filter(user_id=pk).order_by('-id')
    date = request.GET.get("date")

    if date:
        date = parse_date(date)
        attend = attend.filter(date=date)

    return render(request, "checkAttendance.html", {"attend": attend})

@login_required(login_url='index')
def paylistView(request, pk):
    pay = Payroll.objects.filter(employee_id=pk)
    return render(request, "paylistView.html", {"pay": pay})

@login_required(login_url='index')
def ApplyLeave(request, pk):
    data = Employee_data.objects.get(id=pk)
    res = Leave.objects.filter(user_id=pk)
    return render(request, "apply_leave.html", {"res": res,'data':data})

@login_required(login_url='index')
def RequestLeave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            start = leave.startdate
            end = leave.enddate
            leave.user = get_employee(request)
            leave.days = get_leave_duration(start, end) + 1
            leave.save()
            return redirect('applyLeave', pk=get_employee_id(request))
    else:
        form = LeaveForm()
    return render(request, 'RequestLeave.html', {'form': form})

@login_required(login_url='index')
def edit_leave(request,pk):
    if request.method == 'POST':
        res = Leave.objects.get(id=pk)
        form = LeaveForm(request.POST,instance=res)
        if form.is_valid():
            leave = form.save(commit=False)
            start = leave.startdate
            end = leave.enddate
            leave.user = get_employee(request)
            leave.days = get_leave_duration(start, end) + 1
            leave.save()
            return redirect('applyLeave', pk=get_employee_id(request))
    else:
        res = Leave.objects.get(id=pk)
        form = LeaveForm(instance=res)
    return render(request,'edit_leave.html',{'form':form})

@login_required(login_url='index')
def delete_leave(request,pk):
    res = Leave.objects.get(id=pk)
    res.delete()
    return redirect('applyLeave', pk=get_employee_id(request))

@login_required(login_url='index')
def all_attendance_view(request):
    attend = Attendance.objects.all().order_by('-id')
    date = request.GET.get("date")
    if date:
        date = parse_date(date)
        attend = attend.filter(date=date)

    return render(request, "all_attendance_view.html", {"attend": attend})

@login_required(login_url='index')
def employee_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='index')
def viewLeaveRequest(request):
    res = Leave.objects.all()
    return render(request, 'viewLeaveRequest.html', {'res': res})

@login_required(login_url='index')
def ViewLeaveDetails(request, pk):
    leave = get_object_or_404(Leave, id=pk)
    if request.method == 'POST':
        form = LeaveAdminForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('viewLeaveRequest')
    else:
        form = LeaveAdminForm(instance=leave)

    return render(request, 'ViewLeaveDetails.html', {'leave': leave, 'form': form})

@login_required(login_url='index')
def pay(request):
    data = Employee_data.objects.get(user=request.user)
    return render(request,'pay.html',{'data':data})

@login_required(login_url='index')
def approvedLeave(request):
    res = Leave.objects.all()
    return render(request, 'approved.html', {'res': res})

@login_required(login_url='index')
def rejectedLeave(request):
    res = Leave.objects.all()
    return render(request, 'rejected.html', {'res': res})

@login_required(login_url='index')
def contacts_view(request):
    contacts = Employee_data.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts})

@login_required(login_url='index')
def AdminLogOut(request):
    logout(request)
    return redirect('index')

@login_required(login_url='index')
def delete_payslip(request,pk):
    res = Payroll.objects.get(id=pk)
    res.delete()
    return redirect('generate_payslip')
    
import uuid
def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # print(username)

        try:
            user = User.objects.get(username=username)
            # print(user.email)
        except Exception as e:
            # print(e)
            messages.success(request, "User Name is Not Available.")
        else:
            profile_obj = userdetials.objects.get(user=user)
            token = str(uuid.uuid4())
            profile_obj.password_token = token
            profile_obj.save()
            send_forget_password_mail(user.email,token)
            messages.success(request,"An Mail Sent Successfully, Check Your Mail")
            return redirect('forget_password')

    return render(request,'forget_password.html')

def change_password(request,token):
    try:
        profile_obj = userdetials.objects.get(password_token = token)
    except Exception as e:
        return HttpResponse('The Link Has Been Expired')
    # print(profile_obj.user)

    emp = Employee_data.objects.get(user=profile_obj.user)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        reconfirm_password = request.POST.get('reconfirm_password')

        if new_password != reconfirm_password:
            messages.error(request,'Password Doesn\'t Match, Make sure both is Same')
            return redirect(f'change_password/{token}')

        user_obj = User.objects.get(username = profile_obj.user)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('index')

    return render(request,'change_password.html',{'emp':emp})