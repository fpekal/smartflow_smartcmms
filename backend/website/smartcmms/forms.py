from django import forms
from .models import Form, Activity


class FormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['name']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['form', 'name']
