from django.urls import path
from shopapp import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
    path('employee_dashboard/',views.employee_dashboard,name='employee_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('add_admin/',views.add_admin,name='add_admin'),
    path('emp_management/',views.emp_management,name='emp_management'),
    path('customer_management/',views.customer_management,name='customer_management'),
    path('dealer_management/',views.dealer_Management,name='dealer_management'),
    path('medicine_management/',views.medicine_management,name='medicine_management'),
    path('add_dealer/',views.add_dealer,name='add_dealer'),
]