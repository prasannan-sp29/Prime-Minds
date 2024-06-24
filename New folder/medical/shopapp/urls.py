from django.urls import path
from shopapp import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
    path('employee_dashboard/',views.employee_dashboard,name='employee_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('delivery_mang/',views.delivery_management,name='delivery_mang'),
    path('add_admin/',views.add_admin,name='add_admin'),    
    path('emp_management/',views.emp_management,name='emp_management'),
    path('customer_management/',views.customer_management,name='customer_management'),
    path('add_customer/',views.add_customer,name='add_customer'),
    path('dealer_management/',views.dealer_Management,name='dealer_management'),
    # path('add-dealer/',views.add_dealer, name='add_dealer'),
    path('medicine_management/',views.medicine_management,name='medicine_management'),
    path('add_medicine/',views.add_medicine, name='add_medicine'),
    path('sale_mang/',views.sale_management, name='sale_mang'),
    path('new_sale',views.new_sale, name='new_sale'),
    path('get_customer_image/<int:customer_id>/', views.get_customer_image, name='get_customer_image'),



    # path('fetch-emails/',views.fetch_emails_view, name='fetch_emails'),


    # path('index1/',views.index1,name='index1'),
    # path('create-form/',views.create_contace,name='create-contact'),

    path('add_dealer1',views.add_dealer1,name='add_dealer1'),
    path('dealer-form/',views.create_dealer,name='create-dealer'),   

    path('create-sale/',views.create_sale,name='create-sale'), 
    path('create-purchase/',views.add_purchase,name='create-purchase'),    
    
    
    path('purchase_mang',views.purchase_management,name='purchase_mang'),
    path('new_purchase',views.create_purchase,name='new_purchase'),
    # path('index/',views.index,name='index'),
    path('edit_dealer/<int:pk>/',views.edit_dealer,name='edit_dealer'),
    path('delete_dealer/<int:pk>/',views.delete_dealer,name='delete_dealer'),

    path('edit_medicine/<int:pk>/',views.edit_medicine,name='edit_medicine'),
    path('delete_medicine/<int:pk>/',views.delete_medicine,name='delete_medicine'),

    path('edit_employee/<int:pk>/',views.edit_employee,name='edit_employee'),
    path('delete_employee/<int:pk>/',views.delete_employee,name='delete_employee'),

    path('edit_customer/<int:pk>/',views.edit_customer,name='edit_customer'),
    path('delete_customer/<int:pk>/',views.delete_customer,name="delete_customer"),

    path('edit_purchase/<int:pk>/',views.edit_purchase,name='edit_purchase'),
    path('delete_purchase/<int:pk>/',views.delete_purchase,name='delete_purchase'),

    path('edit_sale/<int:pk>/',views.edit_sale,name='edit_sale'),
    path('delete_sale/<int:pk>/',views.delete_sale,name='delete_sale'),

    path('confirm_sale/<int:pk>/', views.confirm_sale, name='confirm_sale'),
    path('confirm_lead/<int:pk>/',views.confirm_lead,name='confirm_lead'),
    path('confirm_opportunity/<int:pk>/',views.confirm_opportunity,name='confirm_opportunity'),
    
    path('confirm/', views.confirm, name='confirm'),    
    path('change_status/', views.change_status, name='change_status'),
    path('delivery_report/<int:pk>/',views.delivery_report,name='delivery_report'),
    path('crm_management/',views.crm_management,name='crm_mang'),
    path('view_lead/',views.view_lead,name='view_lead'),
    path('view_opportunity/',views.view_opportunity,name='view_opportunity'),
    path('view_sale_order/',views.view_sale_order,name='view_sale_order'),
    path('fetch/', views.fetch_and_store_email_data, name='fetch'),


]