from django.shortcuts import render,redirect
from accounts.forms import userForm
from department.models import dept
from django.contrib.auth import authenticate,login
from accounts.models import userdetials
from django.http import HttpResponse
from employee.models import Employee_data


# Create your views here.

def index(request):
    dname = dept.objects.all()
    if request.method == 'POST':
        # name = request.POST.get('op')
        # print(name)
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username)
        # print(password)
        user = authenticate(username=username,password=password)
        print(user)
        print(request.user)
        if user:
            if user.is_active:
                login(request,user)
                d = Employee_data.objects.get(user=user)
                print(d.department)
                
                if str(d.department) == 'admin':
                    print('Login Success')
                
                    return redirect('dashboard')
                else:
                    return redirect('profile')
            else:
                return HttpResponse('User is not Active')
        else:
            return HttpResponse('Please Check Your Creds...!')
    return render(request,'index.html',{'dname':dname})

# def register_details(request):
#     # dname = dept.objects.all()
#     if request.method == 'POST':
#         name = request.POST.get('op')
#         form = userForm(request.POST)
#         # form1= department_details(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.set_password(user.password)
#             user.save()

#             # profile = form1.save(commit=False)
#             # # profile.dept = dname
#             # profile.user = user
#             # profile.save()
#     else:
#         form = userForm()
#         # form1 = department_details()
#     return render(request,'register.html',{'form':form})

def profile(request):
    data = Employee_data.objects.get(user=request.user)
    return render(request,'profile.html',{'data':data})