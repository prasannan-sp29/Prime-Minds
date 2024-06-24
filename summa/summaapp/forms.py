from django import forms
from .models import Category

class CategoryWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'category-widget'})

class CategoryField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(queryset=Category.objects.all(), widget=CategoryWidget(), *args, **kwargs)

    def clean(self, value):
        if not value:
            raise forms.ValidationError('This field is required.')
        if value.isdigit():
            return super().clean(value)
        else:
            category, created = Category.objects.get_or_create(name=value)
            return category
