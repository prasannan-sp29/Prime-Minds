from django import forms
from department.models import dept

class department_form(forms.ModelForm):
    class Meta:
        model = dept
        fields = "__all__"