from django.conf.urls.defaults import *
from django.conf import settings


#from django.contrib import databrowse
from ourcrestmont.itaco.models import *
from ourcrestmont.itaco.forms import ProfileForm


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Media handling
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),   
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),                
    
    # For django-registration (password resets, etc)
    (r'^accounts/', include('registration.backends.default.urls')),    
    
    # Rosters - family and student listings
    (r'^roster/', include('roster.urls')),                 

    # These  URLs route to the same view. The family_detail view will then connect to render_to_csv if /csv/ is present.
    # To get data slices we optionally pass in a named year or a named period or the static var "all" (to view all billing periods)
    url(r'^family/(?P<fam_id>\d+)/?$', 'ourcrestmont.itaco.views.family_detail', name='family_detail'),
    url(r'^family/(?P<fam_id>\d+)/contact/?$', 'ourcrestmont.itaco.views.family_contact', name='family_contact'),
    url(r'^family/(?P<fam_id>\d+)/year/(?P<year>\d+)/?$', 'ourcrestmont.itaco.views.family_detail', name='family_detail_yr'),    
    url(r'^family/(?P<fam_id>\d+)/period/(?P<period>\d+)/?$', 'ourcrestmont.itaco.views.family_detail', name='family_detail_prd'),
    url(r'^family/(?P<fam_id>\d+)/all/?$', 'ourcrestmont.itaco.views.family_detail', {'all':"all"}, name='family_detail_all'),            

    # Same views but for CSV. Unfortunately we can't just represent these with a single entry .*(?P<csv>csv)
    # because we'd lose the parameters for specifying the particular billing view.
    url(r'^family/(?P<fam_id>\d+)/(?P<csv>csv)/?$', 'ourcrestmont.itaco.views.family_detail', name='family_detail_csv'),
    url(r'^family/(?P<fam_id>\d+)/year/(?P<year>\d+)/(?P<csv>csv)/?$', 'ourcrestmont.itaco.views.family_detail', name='family_detail_csv_yr'),    
    url(r'^family/(?P<fam_id>\d+)/period/(?P<period>\d+)/(?P<csv>csv)/?$', 'ourcrestmont.itaco.views.family_detail', name='family_detail_csv_prd'),
    url(r'^family/(?P<fam_id>\d+)/all/(?P<csv>csv)/?$', 'ourcrestmont.itaco.views.family_detail', {'all':"all"}, name='family_detail_csv_all'),    


    # Misc administrative tools, such as batch daycare charge entry and billing summary
    url(r'^tools/charges/daycare/$', 'ourcrestmont.itaco.views.batch_daycare_charges', name='batch_daycare_charges'),
    url(r'^tools/charges/participation/$', 'ourcrestmont.itaco.views.batch_participation_credits', name='batch_participation_credits'),    
    url(r'^tools/obligations/$', 'ourcrestmont.itaco.views.batch_obl', name='batch_obl'),    
    url(r'^tools/credits/board/$', 'ourcrestmont.itaco.views.batch_board_credit', name='batch_board_credit'),
    
    url(r'^tools/credits/board/period/(?P<period>\d+)/$', 'ourcrestmont.itaco.views.batch_board_credit', name='batch_board_credit_period'),    
    url(r'^tools/credits/board/period/(?P<period>\d+)/apply/?$', 'ourcrestmont.itaco.views.batch_board_credit', {'apply':True}, name='batch_board_credit_apply'),  

    url(r'^tools/billing_summary/period/(?P<period>\d+)/?$', 'ourcrestmont.itaco.views.summary_charges_credits', name='summary_charges_credits'),  
    url(r'^tools/billing_summary/$', 'ourcrestmont.itaco.views.summary_charges_credits', name='summary_charges_credits'),  
    url(r'^tools/billing_summary/(?P<csv>csv)/period/(?P<period>\d+)/$', 'ourcrestmont.itaco.views.summary_charges_credits', name='csv_summary_charges_credits'), 

    # Administrator's view of all obligations owed on one page
    url(r'^tools/obligation_summary/$', 'ourcrestmont.itaco.views.obligation_summary', name='obligation_summary'), 
    
    # Generate mailing list members
    url(r'^lists/$', 'ourcrestmont.itaco.views.listgen', name='listgen'),          
      

    # Admin, databrowse, filebrowser
    (r'^admin/', include(admin.site.urls)),
    #(r'^databrowse/(.*)', databrowse.site.root),
    
    
    # Profile editing
    # First match /profiles/edit before django-profiles gets it and loads the defaults, so we can pass in our custom form object.
    ('^profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^profiles/', include('profiles.urls')),
    url(r'^student/(?P<student_id>\d+)/edit/?$', 'ourcrestmont.itaco.views.edit_student', name='edit_student'),      

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/flower.gif'}),
)

