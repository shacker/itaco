from django.conf.urls.defaults import *
from ourcrestmont.apply.views import *

urlpatterns = patterns('apply.views',

    url(r'^/?$', 'apply', name='apply'),
    url(r'^process_apps/?$', 'process_apps', name='process_apps'),    
    url(r'^app/(?P<app_id>\d+)/?$', 'app_detail', name='app_detail'),
)




