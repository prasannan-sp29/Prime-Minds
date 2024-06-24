from django import forms
from django.contrib.auth.models import User
from shopapp.models import *
from django.forms import inlineformset_factory

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

class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ['first_name','last_name','username','password','address','city','state','pincode','phone_number','mail_id','profile_picture']

class CustomerForm1(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name','last_name','address','city','state','pincode','phone_number','mail_id','profile_picture']


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = '__all__'

class TabletForm(forms.ModelForm):
    class Meta:
        model = Tablet
        fields = ['tablet_name', 'price']

TabletFormSet = inlineformset_factory(Dealer, Tablet, form=TabletForm, extra=1)

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['name', 'phone_number']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'medicine','phone', 'price', 'quantity', 'discount', 'tax']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['customer', 'phone']

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['tablet', 'price', 'quantity']

PurchaseItemFormSet = inlineformset_factory(Purchase, PurchaseItem, form=PurchaseItemForm, extra=1)

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