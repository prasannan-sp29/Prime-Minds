# fields.py

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

class ForeignKeyCharField(forms.CharField):
    def __init__(self, model: Model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value.strip() == '':
            return None

        try:
            return self.model.objects.get(pk=value)
        except (ValueError, ObjectDoesNotExist):
            return value

    def prepare_value(self, value):
        if isinstance(value, Model):
            return str(value.pk)
        return value
