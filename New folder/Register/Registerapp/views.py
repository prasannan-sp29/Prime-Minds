from django.shortcuts import render

# Create your views here.

def user_reg(request):
    return render(request,'register.html',{})
