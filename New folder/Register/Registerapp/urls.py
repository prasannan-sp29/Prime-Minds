from django.urls import path
from Registerapp import views

urlpatterns = [
    path('',views.user_reg,name='register'),
]