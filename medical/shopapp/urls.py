from django.urls import path
from shopapp import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
]