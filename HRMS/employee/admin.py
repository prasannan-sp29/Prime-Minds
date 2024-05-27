from django.contrib import admin
from employee.models import Employee_data,Payroll,Attendance,Leave

# Register your models here.

admin.site.register(Employee_data)
admin.site.register(Payroll)
admin.site.register(Attendance)
admin.site.register(Leave)