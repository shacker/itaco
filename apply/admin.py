from apply.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib import messages

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('child_last','child_first','grade','appdate','rq_start_date','eval_date')
    list_filter = ('grade',)

admin.site.register(Application, ApplicationAdmin)
