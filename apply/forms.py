from django.db import models
from django.forms import ModelForm
from django import forms
from apply.models import Application


class ApplicationForm(ModelForm):

    # Need a custom CSS class on some fields to make them shorter
    prev_school1 = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school2 = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school3 = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school1_dates = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school2_dates = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school3_dates = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school1_phone = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school2_phone = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))
    prev_school3_phone = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'shortfield'}))    
    
    error_css_class = 'error'
    required_css_class = 'required'    
    
    class Meta:
        model = Application
        exclude = ('appdate','accepted','fee_paid','status','teacher_rec_form')


class AppEditForm(ModelForm):
    # Full application edit form, for superusers only
    class Meta:
        model = Application
        widgets = {'teacher_rec_form': forms.FileInput}
        fields = ('teacher_rec_form','fee_paid','attended_tour','eval_date','status','staff_notes')



class TeacherAppEditForm(ModelForm):
    # Minimal application edit form, mostly just for teachers
    class Meta:
        model = Application
        widgets = {'teacher_rec_form': forms.FileInput}
        fields = ('staff_notes',)
