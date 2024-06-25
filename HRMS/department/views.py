from django.shortcuts import render,redirect
from department.forms import department_form
from department.models import dept
from employee.models import Employee_data
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='index')
def add_department(request):
    d = dept.objects.all()
    if request.method == 'POST':
        form = department_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addDepartment')
    else:
        form = department_form()
    return render(request,'add_department.html',{'form':form,'d':d})

@login_required(login_url='index')
def del_department(request,pk):
    res = dept.objects.get(id=pk)

    res.delete()
    return redirect('addDepartment')

@login_required(login_url='index')
def department_view(request,pk):
    data = Employee_data.objects.filter(department_id = pk)
    return render(request,'department_view.html',{'data':data})

@login_required(login_url='index')
def department_delete(request,pk):
    res = dept.objects.get(id=pk)
    res.delete()
    return redirect('addDepartment')