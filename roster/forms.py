from django.db import models
from django import forms
from django.forms import ModelForm

class SearchForm(ModelForm):
    """Search rosters"""

    q = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'size':35})
    )