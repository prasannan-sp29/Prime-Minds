from django import forms
from django.contrib.auth.models import User
from accounts.models import userdetials

class userForm(forms.ModelForm):
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

# class department_details(forms.ModelForm):
#     class Meta:
#         model = userdetials
#         fields = ['department_name']