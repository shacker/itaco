from django.conf.urls.defaults import *
from apply.views import *

urlpatterns = patterns('apply.views',

    url(r'^/?$', 'apply', name='apply'),
       
)





