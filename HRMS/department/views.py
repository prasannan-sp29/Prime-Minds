from django.shortcuts import render,redirect
from department.forms import department_form
from department.models import dept
from employee.models import Employee_data

# Create your views here.

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

def del_department(request,pk):
    res = dept.objects.get(id=pk)

    res.delete()
    return redirect('addDepartment')

def department_view(request,pk):
    data = Employee_data.objects.filter(department_id = pk)
    return render(request,'department_view.html',{'data':data})