from django.db import models
from django.forms import ModelForm
from django import forms
from ourcrestmont.apply.models import Application

class ApplicationForm(ModelForm):
    # family = forms.ModelChoiceField(queryset=Family.has_students.all())
    # amount = forms.FloatField(help_text='')

    class Meta:
        model = Application
        exclude = ('appdate','accepted',)
