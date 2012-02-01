from apply.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib import messages

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('child_last','child_first','appdate','rq_start_date','eval_date')

admin.site.register(Application, ApplicationAdmin)
