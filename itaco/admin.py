from ourcrestmont.itaco.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

class StudentAdmin(admin.ModelAdmin):
    # search_fields = ['last_name','first_name']
    # list_display = ('last_name','first_name','expected_grad_yr','reader','enrolled',)
    # exclude = ('groups',) 
    search_fields = ['first_name','last_name']
    list_display = ('last_name','first_name','family','expected_grad_yr',)
    

class ParentAdmin(admin.ModelAdmin):
    # list_display = ('get_user_display','family','address1',)
    # exclude = ('groups',) 
    search_fields = ['user__last_name','user__first_name']
    raw_id_fields = ('user', )
    list_display = ('parent_name','title','participating_parent','no_lists',)
    list_editable = ('participating_parent',)
    
    
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('family','fa_factor',)
    search_fields = ['name']
    
class CreditAdmin(admin.ModelAdmin):
    list_display = ('family','date','type','amount',)
    search_fields = ['family__name',]
    list_filter = ('type',)    
    
class ObligationAdmin(admin.ModelAdmin):
    list_display = ('family','date','type','amount','units',)
    search_fields = ['family__name',]
    list_filter = ('type',)    
    
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('family','date','type','amount','charged_amount',) 
    exclude = ('units',)    
    search_fields = ['family__name',]
    list_filter = ('type',)
    
class ListExtraAdmin(admin.ModelAdmin):
    ordering = ('list',)

    
class BoardPositionAdmin(admin.ModelAdmin):
    list_display = ('title','credit')    
    
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ('title','grad_class','current')
    admin_order_field = ('-title',)


class BillingPeriodAdmin(admin.ModelAdmin):
    list_display = ('title','school_year','start','end')  
    
      
    
admin.site.register(CommitteeJob) 
admin.site.register(ListExtra,ListExtraAdmin) 
admin.site.register(Family,FamilyAdmin)    
admin.site.register(Parent,ParentAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Credit,CreditAdmin)
admin.site.register(Obligation,ObligationAdmin)
admin.site.register(Charge,ChargeAdmin)
admin.site.register(BoardPosition,BoardPositionAdmin)
admin.site.register(SchoolYear,SchoolYearAdmin)
admin.site.register(BillingPeriod,BillingPeriodAdmin)


# TinyMCE for flatpages, per http://code.djangoproject.com/wiki/AddWYSIWYGEditor
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

class FlatPageAdmin(FlatPageAdminOld):
    class Media:
        js = (
                'js/tiny_mce/tiny_mce.js',
                'js/textareas.js',
            )

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
