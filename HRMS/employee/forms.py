from django import forms
from employee.models import *
import datetime

class add_employee_form(forms.ModelForm):
    class Meta:
        model = Employee_data
        fields = ['profile_picture', 'name','emp_code', 'DOB', 'date_of_join', 'address', 'city', 'pincode', 'phone_number','alternate_phone_number','aadhar_no', 'state', 'mail_id', 'pan_number', 'department', 'salary',
        'bank_name','bank_acc_number']
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
            'date_of_join': forms.DateInput(attrs={'type': 'date'}),
        }
        
class PayrollForm(forms.ModelForm):
    month = forms.DateField(
        widget=forms.DateInput(format='%Y-%m', attrs={'type': 'month'}),
        input_formats=['%Y-%m']
    )

    class Meta:
        model = Payroll
        fields = ['month']
        # widgets = {
        #     'month': forms.DateInput(attrs={'type': 'month'}),
        # }

class LeaveForm(forms.ModelForm):
    reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = Leave
        fields = ['user', 'startdate', 'enddate', 'leavetype', 'reason']
        widgets = {
            'startdate': forms.DateInput(attrs={'type': 'date'}),
            'enddate': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_enddate(self):
        enddate = self.cleaned_data.get('enddate')
        startdate = self.cleaned_data.get('startdate')
        today_date = datetime.date.today()

        if startdate and enddate:
            if startdate < today_date or enddate < today_date:
                raise forms.ValidationError("Selected dates are incorrect, please select again")

            if startdate >= enddate:
                raise forms.ValidationError("Start date must be before end date")

        return enddate

class LeaveAdminForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['status']