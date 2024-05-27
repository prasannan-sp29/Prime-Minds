from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import userdetials
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from employee.models import Employee_data, Payroll, Attendance, Leave
from employee.forms import *
from django.http import HttpResponse
from .forms import PayrollForm
from django.utils import timezone
from .models import Attendance
from django.http import JsonResponse
from django.contrib import messages
import pytz
from django.utils.dateparse import parse_date


# Create your views here.
def dashboard(request):
    # data = Employee_data.objects.all()
    return render(request, "admin_dashboard.html")


def employeeDetails(request):
    data = Employee_data.objects.all()
    return render(request, "employee_details.html", {"data": data})


def know_more(request, pk):
    data = Employee_data.objects.get(id=pk)
    return render(request, "know_more.html", {"data": data})


def remove_space(inp_str):
    op_str = inp_str.replace(" ", "").lower()
    return op_str


def add_employee(request):
    if request.method == "POST":
        form = add_employee_form(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            username = remove_space(employee.name)
            email = employee.mail_id
            password = username[:4] + str(employee.phone_number)[-4:]
            # create user
            user = User.objects.create_user(
                username=username, email=email, password=password
            )

            employee.user = user
            employee.id = user.id
            employee.save()

            # create user details
            userdetials.objects.create(user=user)

            return redirect("employee_details")
    else:
        form = add_employee_form()
    return render(request, "add_employee.html", {"form": form})


def edit_profile(request, pk):
    if request.method == "POST":
        data = Employee_data.objects.get(id=pk)
        form = add_employee_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect("know_more", pk)
    else:
        data = Employee_data.objects.get(id=pk)
        form = add_employee_form(instance=data)
    return render(request, "edit_profile.html", {"form": form})


def get_employee(request):
    employee = Employee_data.objects.get(user=request.user)
    return employee

def get_employee_id(request):
    employee = Employee_data.objects.get(user=request.user)
    return employee.id


def generate_payslip(request):
    pay = Payroll.objects.all().order_by('-id')
    employees = Employee_data.objects.all()
    if request.method == "POST":
        form = PayrollForm(request.POST)
        if form.is_valid():

            for i in employees:
                MONTH = form.cleaned_data["month"]
                # print(MONTH)
                ctc = i.salary
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
                Total_gross = Gross_salary - (PF + IT + PT)

                p = Payroll(
                    employee=i,
                    month=MONTH,
                    basic=basic,
                    hra=HRA,
                    da=DA,
                    ta=TA,
                    pf=PF,
                    income_tax=IT,
                    professional_tax=PT,
                    gross=Gross_salary,
                    total_gross=Total_gross,
                )
                p.save()
            print("Payroll Saved successfully for all employees")
            messages.warning(request,"Payroll Generated Successfully for all Employees.")
            # return JsonResponse({"message": "Payroll Generated Successfully."}, safe=False)
            # return redirect('generate_payslip_pdf', pk=p.id)
    else:
        form = PayrollForm()
    return render(
        request, "generate_payslip.html", {"form": form, "pay": pay}
    )


def single_payslip(request):
    data = Employee_data.objects.all()
    if request.method == "POST":
        form = PayrollForm(request.POST)
        if form.is_valid():
            MONTH = form.cleaned_data["month"]
            # print(MONTH)
            ctc = data.salary
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
            Total_gross = Gross_salary - (PF + IT + PT)

            p = Payroll(
                employee=data,
                month=MONTH,
                basic=basic,
                hra=HRA,
                da=DA,
                ta=TA,
                pf=PF,
                income_tax=IT,
                professional_tax=PT,
                gross=Gross_salary,
                total_gross=Total_gross,
            )
            p.save()
            print("Payroll created successfully for single employee")
        # return redirect('generate_payslip_pdf', pk=p.id)
    else:
        form = PayrollForm()
    return render(
        request, "single_payslip.html", {"form": form,}
    )


def generate_payslip_pdf(request, pk):
    # data = Employee_data.objects.get(name=request.name)
    slip = Payroll.objects.get(id=pk)
    end_of_month = slip.get_end_of_month()
    return render(request, "payslip_template.html", {"slip": slip,'end_of_month':end_of_month})


def attendacne_view(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        action = request.POST.get("action")

        try:
            user1 = User.objects.get(username=user_name)
            try:
                user = Employee_data.objects.get(user_id=user1.id)
            except Employee_data.DoesNotExist:
                return JsonResponse({"message": "User not found."}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found."}, safe=False)

        today = timezone.now().date()
        ist = pytz.timezone("Asia/Kolkata")

        attendance, created = Attendance.objects.get_or_create(user=user, date=today)

        if action == "check-in" and attendance.check_in_time is None:
            check_in_time = timezone.now().astimezone(ist).time()
            attendance.check_in_time = check_in_time
            attendance.save()
            return JsonResponse({"message": "Check-in successful."}, safe=False)

        elif action == "check-out" and attendance.check_out_time is None:
            check_out_time = timezone.now().astimezone(ist).time()
            attendance.check_out_time = check_out_time
            attendance.save()
            return JsonResponse({"message": "Check-out successful."}, safe=False)

        return JsonResponse(
            {"message": "Action already recorded or invalid."}, safe=False
        )

    return render(request, "attendance.html")


def deleteEmployee(request, pk):
    res = Employee_data.objects.get(id=pk)
    del_user = User.objects.get(id=pk)
    u = userdetials.objects.get(user_id=pk)
    del_user.delete()
    u.delete()
    res.delete()
    return redirect("employee_details")


def checkAttendance(request, pk):
    attend = Attendance.objects.filter(user_id=pk)
    date = request.GET.get("date")

    if date:
        date = parse_date(date)
        attend = attend.filter(date=date)

    context = {"attend": attend}

    return render(request, "checkAttendance.html", {"attend": attend})


def paylistView(request, pk):
    pay = Payroll.objects.filter(employee_id=pk)
    return render(request, "paylistView.html", {"pay": pay})


def ApplyLeave(request, pk):
    res = Leave.objects.filter(user_id=pk)
    return render(request, "apply_leave.html", {"res": res})


def RequestLeave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = get_employee(request)
            leave.save()
            return redirect('applyLeave',pk=get_employee_id(request))
    else:
        form = LeaveForm()
    return render(request,'RequestLeave.html',{'form':form})


def all_attendance_view(request):
    attend = Attendance.objects.all()
    date = request.GET.get("date")

    if date:
        date = parse_date(date)
        attend = attend.filter(date=date)

    context = {"attend": attend}
    return render(request, "all_attendance_view.html", context)


def employee_profile(request, pk):
    data = Employee_data.objects.get(id=pk)
    return render(request, "employee_profile.html", {"data": data})

def employee_logout(request):
    logout(request)
    return redirect('index')

def viewLeaveRequest(request):
    res = Leave.objects.all()
    return render(request,'viewLeaveRequest.html',{'res':res})

def ViewLeaveDetails(request,pk):
    leave = Leave.objects.get(id=pk)
    leave_duration = leave.get_leave_duration()
    if request.method == 'POST':
        form = LeaveAdminForm(request.POST,instance=leave)
        if form.is_valid():
            form.save()

    else:
        form = LeaveAdminForm(instance=leave)

    return render(request,'ViewLeaveDetails.html',{'leave':leave,'form':form,'leave_duration':leave_duration})

def approvedLeave(request):
    res = Leave.objects.all()
    return render(request,'approved.html',{'res':res})

def rejectedLeave(request):
    res = Leave.objects.all()
    return render(request,'rejected.html',{'res':res})

def contacts_view(request):
    contacts = Employee_data.objects.all()
    return render(request,'contacts.html',{'contacts':contacts})

def AdminLogOut(request):
    logout(request)
    return redirect('index')
