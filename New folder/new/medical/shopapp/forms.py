from django import forms
from django.contrib.auth.models import User
from shopapp.models import *
from django.core.exceptions import ValidationError
import re

class userForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['profile_picture','emp_id','first_name','last_name','mail_id','phone_number','address','salary']

    def clean_phone_number(self):
        phone_number = str(self.cleaned_data.get('phone_number'))
        if not re.fullmatch(r'\d{10}', phone_number):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return int(phone_number)


class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['first_name','last_name','username','password','address','city','state','pincode','phone_number','mail_id','profile_picture']

class CustomerForm1(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name','last_name','address','city','state','pincode','phone_number','mail_id','profile_picture']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','phone']


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name','medicine_code','dealer_name','stock','company_name','description']

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = '__all__'

class TabletForm(forms.ModelForm):
    class Meta:
        model = Tablet
        fields = ['tablet_name','price']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer','phone', 'discount', 'tax','confirmed']
        widgets = {
            'customer': forms.Select(attrs={'onchange': 'updateCustomerImage()'}),
        }

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['medicine','price','quantity']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['dealer','phone']

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['tablet_name','price','quantity']   
        widgets = {
            'medicine': forms.Select(attrs={'id': 'id_medicine'}),
        }    

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = '__all__'

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder  
        fields = '__all__'                  