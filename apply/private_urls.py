from django.conf.urls.defaults import *
from apply.views import *

urlpatterns = patterns('apply.views',

    url(r'^process_apps/?$', 'process_apps', name='process_apps'),    
    url(r'^send_offer/(?P<app_id>\d+)/?$', 'send_offer', name='app_send_offer'),
    url(r'^send_eval/(?P<app_id>\d+)/?$', 'send_eval_letter', name='app_send_eval'),    
    url(r'^intake/(?P<app_id>\d+)/?$', 'intake', name='app_intake'),        
    url(r'^(?P<app_id>\d+)/?$', 'app_detail', name='app_detail'),
    url(r'^show_addrs/?$', 'show_addrs', name='show_addrs'),        
)





