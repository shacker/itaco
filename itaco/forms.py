from django.db import models
from django.forms import ModelForm
from django import forms
from ourcrestmont.itaco.models import *


class ChargeForm(ModelForm):
    family = forms.ModelChoiceField(queryset=Family.has_students.all())

    class Meta:
        model = Charge
        exclude = ('units','type','date','charged_amount',)

        
# class MaintOblForm(ModelForm):
#     family = forms.ModelChoiceField(queryset=Family.has_students.all())
#     amount = forms.FloatField(help_text='')
# 
#     class Meta:
#         model = Obligation
#         exclude = ('units','type','date','charged_amount',)  

class OblForm(ModelForm):
    family = forms.ModelChoiceField(queryset=Family.has_students.all())
    amount = forms.FloatField(help_text='')

    class Meta:
        model = Obligation
        exclude = ('units','type','date','charged_amount',)      

        
class PartCredForm(ModelForm):
    
    # Participation Credits
    family = forms.ModelChoiceField(queryset=Family.has_students.all())
    amount = forms.FloatField(label="Hours")

    class Meta:
        model = Credit
        # family = Family.has_students.all()
        exclude = ('units','type','date','charged_amount',)

    
class CreditForm(ModelForm):
    class Meta:
        model = Credit
        
class StudentForm(ModelForm):
    
    class Meta:
        model = Student
        fields = ('birthdate',)
        

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
        except User.DoesNotExist:
            pass
 
    email = forms.EmailField(label="Primary email", help_text="Used for school mailing lists. <br />Changes may not be reflected on lists immediately.")
  
    class Meta:
      model = Profile
      exclude = ('family','user','board_pos','comm_job',)
      fields = (
               'about',
               'avatar',
               'email',
               'email_2',
               'address1',
               'address2',
               'city',
               'state',
               'zip',
               'phone_home',
               'phone_work',
               'phone_mobile',
               'twitter',
               'facebook',   
               'url_title',
               'url',            
               'fax',
               'primary_contact',
               )
      
    def save(self, *args, **kwargs):
      """
      Update the primary email address on the related User object as well. 
      """
      u = self.instance.user
      u.email = self.cleaned_data['email']
      u.save()
      profile = super(ProfileForm, self).save(*args,**kwargs)
      return profile
          
      
