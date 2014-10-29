from django.contrib import admin
from accounts.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__last_name','user__first_name']
    raw_id_fields = ('user', )
    list_display = ('profile_name','title','participating_parent','no_lists',)
    list_editable = ('participating_parent',)
    filter_horizontal = ('list_extras','comm_job','board_pos')


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0

admin.site.register(Profile,ProfileAdmin)
