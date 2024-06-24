from django import forms
from employee.models import *
import datetime
from django.core.exceptions import ValidationError
import re

class add_employee_form(forms.ModelForm):
    class Meta:
        model = Employee_data
        fields = ['profile_picture', 'name','emp_code', 'DOB','gender', 'date_of_join', 'permenant_address','current_address', 'phone_number','aadhar_no', 'mail_id', 'pan_number', 'department', 'salary',
        'bank_name','bank_acc_number','emergency_contact_number','emergency_contact_name','emergency_contact_relationship','ifsc_code']
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
            'date_of_join': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_pan_number(self):
        pan_number = str(self.cleaned_data.get('pan_number')).upper()
        if not re.fullmatch(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', pan_number):
            raise ValidationError('PAN number must be exactly 10 characters: 5 letters, 4 digits, and 1 letter. At Upper Case')
        return pan_number
        
    def clean_aadhar_no(self):
        aadhar_no = str(self.cleaned_data.get('aadhar_no'))
        if not re.fullmatch(r'\d{12}',aadhar_no):
            raise ValidationError('Aadhar number must be Exactly 12 digits.')
        return aadhar_no

    def clean_phone_number(self):
        phone_number = str(self.cleaned_data.get('phone_number'))
        if not re.fullmatch(r'\d{10}', phone_number):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone_number

    # def clean_alternate_phone_number(self):
    #     alternate_phone_number = str(self.cleaned_data.get('alternate_phone_number'))
    #     if alternate_phone_number and not re.fullmatch(r'\d{10}', alternate_phone_number):
    #         raise ValidationError("Alternate phone number must be exactly 10 digits.")
    #     return alternate_phone_number

    def clean_emergency_contact_number(self):
        emergency_contact_number = str(self.cleaned_data.get('emergency_contact_number'))
        if not re.fullmatch(r'\d{10}', emergency_contact_number):
            raise ValidationError("Emergency contact number must be exactly 10 digits.")
        return emergency_contact_number


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