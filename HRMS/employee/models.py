from django.db import models
from department.models import dept
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import calendar
from datetime import datetime

# Create your models here.
class Employee_data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    emp_code = models.IntegerField()
    DOB = models.DateField()
    date_of_join = models.DateField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone_number = models.BigIntegerField()
    alternate_phone_number = models.BigIntegerField(blank=True)
    bank_name = models.CharField(max_length=50)
    bank_acc_number = models.BigIntegerField()
    mail_id = models.EmailField()
    aadhar_no = models.BigIntegerField()
    pan_number = models.CharField(max_length=20)
    department = models.ForeignKey(dept, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile', blank=True)
    salary = models.BigIntegerField()

    def __str__(self):
        return self.name


class Payroll(models.Model):
    employee = models.ForeignKey(Employee_data, on_delete=models.CASCADE, null=True, blank=True)
    month = models.DateField()
    basic = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    da = models.DecimalField(max_digits=10, decimal_places=2)
    ta = models.DecimalField(max_digits=10, decimal_places=2)
    pf = models.DecimalField(max_digits=10, decimal_places=2)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2)
    gross = models.DecimalField(max_digits=10, decimal_places=2)
    total_gross = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.employee.name

    def get_month(self):
        date_obj = datetime.strptime(str(self.month), '%Y-%m-%d')
        return date_obj.month

    def get_year(self):
        date_obj = datetime.strptime(str(self.month), '%Y-%m-%d')
        return date_obj.year

    def get_end_of_month(self):
        date_obj = datetime.strptime(str(self.month), '%Y-%m-%d')
        last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
        end_of_month = datetime(date_obj.year, date_obj.month, last_day).date()
        return end_of_month
        

class Attendance(models.Model):
    user = models.ForeignKey(Employee_data, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.user.name

# Leave Module
SICK = 'sick'
CASUAL = 'casual'
EMERGENCY = 'emergency'
STUDY = 'study'

LEAVE_TYPE = (
    (SICK, 'Sick Leave'),
    (CASUAL, 'Casual Leave'),
    (EMERGENCY, 'Emergency Leave'),
    (STUDY, 'Study Leave'),
)

STATUS = (
    ('Approved','Approved'),
    ('Pending','Pending'),
    ('Rejected','Rejected'),
)

DAYS = 30

class Leave(models.Model):
    user = models.ForeignKey(Employee_data, on_delete=models.CASCADE, blank=True)
    startdate = models.DateField(verbose_name=_('Start Date'), help_text='leave start date is on ..', null=True, blank=False)
    enddate = models.DateField(verbose_name=_('End Date'), help_text='coming back on ...', null=True, blank=False)
    days = models.IntegerField()
    leavetype = models.CharField(choices=LEAVE_TYPE, max_length=25, default=SICK, null=True, blank=False)
    reason = models.CharField(verbose_name=_('Reason for Leave'), max_length=255, help_text='add additional information for leave', null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=15, default='Pending') # pending, approved, rejected, cancelled
    is_approved = models.BooleanField(default=False) # hide
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.name

    # def get_leave_duration(self):
    #     return (self.enddate - self.startdate).days

    # def save(self, *args, **kwargs):
    #     self.leave_duration = self.get_leave_duration()
    #     super().save(*args, **kwargs)