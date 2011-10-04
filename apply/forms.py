from django.db import models
from django.forms import ModelForm
from django import forms
from ourcrestmont.apply.models import Application


class ApplicationForm(ModelForm):
    # family = forms.ModelChoiceField(queryset=Family.has_students.all())
    # amount = forms.FloatField(help_text='')

    # Need a custom CSS class on some fields to make them shorter
    prev_school1 = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school2 = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school3 = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school1_dates = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school2_dates = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school3_dates = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school1_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school2_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school3_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'shortfield'}))
    # attended_tour = forms.CharField(widget=forms.TextInput())
    # attended_tour = forms.ChoiceField(widget=forms.NullBooleanSelect, choices=YESNO_CHOICES)
    
    class Meta:
        model = Application
        exclude = ('appdate','accepted','fee_paid','status','teacher_rec_form')




class AppEditForm(ModelForm):

    class Meta:
        model = Application
        fields = ('fee_paid','eval_date','status','staff_notes')
