from django.conf.urls.defaults import *
from ourcrestmont.apply.views import *

urlpatterns = patterns('apply.views',

    url(r'^/?$', 'apply', name='apply'),
    url(r'^process_apps/?$', 'process_apps', name='process_apps'),    
    url(r'^app/send_offer/(?P<app_id>\d+)/?$', 'send_offer', name='app_send_offer'),
    url(r'^app/send_eval/(?P<app_id>\d+)/?$', 'send_eval_letter', name='app_send_eval'),    
    url(r'^app/(?P<app_id>\d+)/?$', 'app_detail', name='app_detail'),
    # url(r'^app/change/?$', 'change_app_status', name='change_app_status'),  
    # url(r'^app/edit/?$', 'app_edit', name='app_edit'),       
    url(r'^app/show_addrs/?$', 'show_addrs', name='show_addrs'),        
)





