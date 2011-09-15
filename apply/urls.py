from django.conf.urls.defaults import *
from ourcrestmont.apply.views import *

urlpatterns = patterns('apply.views',

    url(r'^/?$', 'apply', name='apply'),
    url(r'^process_apps/?$', 'process_apps', name='process_apps'),    
    url(r'^app/(?P<app_id>\d+)/?$', 'app_detail', name='app_detail'),
    url(r'^app/change/?$', 'change_app_status', name='change_app_status'),   
    url(r'^app/show_addrs/?$', 'show_addrs', name='show_addrs'),        
)





