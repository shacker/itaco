from django.conf.urls.defaults import *
from roster.views import *


urlpatterns = patterns('roster.views',


    url(r'^families/?$', 'roster_families', name='roster_families'),
    url(r'^parents/list/?$', 'roster_parents', name='roster_parents_list'),    
    url(r'^parents/?$', 'roster_parents', {'faces':True}, name='roster_parents_faces'),        
    url(r'^students/k/?$', 'roster_students_kinder', name='roster_students_kinder'),
    url(r'^students/1/?$', 'roster_students_1st', name='roster_students_1st'),    
    url(r'^students/2/?$', 'roster_students_2nd', name='roster_students_2nd'),    
    url(r'^students/3/?$', 'roster_students_3rd', name='roster_students_3rd'),    
    url(r'^students/4/?$', 'roster_students_4th', name='roster_students_4th'),    
    url(r'^students/5/?$', 'roster_students_5th', name='roster_students_5th'),                        
    url(r'^students/?$', 'roster_students', name='roster_students'),
    url(r'^teachers/?$', 'roster_teachers', name='roster_teachers'),
    url(r'^participators/?$', 'roster_participators', name='roster_participators'),      
    url(r'^board/?$', 'roster_board', name='roster_board'),     
    url(r'^jobs/?$', 'roster_jobs', name='roster_jobs'),   
    url(r'^print/?$', 'roster_print', name='roster_print'),
    url(r'^export/?$', 'roster_export', name='roster_export'),        
    url(r'^vcard/multi/?$', 'vcard_multi', name='vcard_multi'),    
    url(r'^vcard/(?P<username>\w+)/?$', 'vcard_single', name='vcard_single'),    
    url(r'^signin/?$', 'signin_print', name='signin_print'),        
)





