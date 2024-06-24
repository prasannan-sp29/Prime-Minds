from django import forms
from pagesapp.models import register_user


class reg_form(forms.ModelForm):
    class Meta:
        model = register_user
        fields = ['fullname','username','email','password']