from django.urls import path
from employee import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('employee_details',views.employeeDetails,name='employee_details'),
    path('addEmployee/',views.add_employee,name='addEmployee'),
    path('know_more/<int:pk>/',views.know_more,name='know_more'),
    path('edit_profile/<int:pk>/',views.edit_profile,name='edit_profile'),
    path('generate_payslip/', views.generate_payslip, name='generate_payslip'),
    path('single_payslip/', views.single_payslip, name='single_payslip'),
    path('generate_payslip_pdf/<int:pk>/', views.generate_payslip_pdf, name='generate_payslip_pdf'),
    path('attendance/',views.attendacne_view,name='attendance'),
    path('deleteEmployee/<int:pk>/',views.deleteEmployee,name='delete_emp'),
    path('viewAttendance/<int:pk>/',views.checkAttendance,name='viewAttendance'),
    path('paylistView/<int:pk>/',views.paylistView,name='paylistView'),
    path('applyLeave/<int:pk>/',views.ApplyLeave,name='applyLeave'),
    path('requestLeave',views.RequestLeave,name='requestLeave'),
    path('allAttendanceView/',views.all_attendance_view,name='allAttendanceView'),
    path('employee_profile/<int:pk>',views.employee_profile,name='employee_profile'),
    path('employee_logout/',views.employee_logout,name='employee_logout'),
    path('viewLeaveRequest/',views.viewLeaveRequest,name='viewLeaveRequest'),
    path('ViewLeaveDetails/<int:pk>',views.ViewLeaveDetails,name='ViewLeaveDetails'),
    path('contacts/',views.contacts_view,name='contacts'),
    path('AdminLogOut/',views.AdminLogOut,name='AdminLogOut'),
    path('approved_leave/',views.approvedLeave,name='approved_leave'),
    path('rejected_leave/',views.rejectedLeave,name='rejected_leave'),

]