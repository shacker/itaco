from django.conf.urls import patterns, url, include
from apply.views import *

# These URLs are visible without iTaco login
urlpatterns = patterns('apply.views',

    url(r'^app_fee/thanks/(?P<app_id>\d+)/?$', 'app_fee_thanks', name='app_fee_thanks'),
    url(r'^app_fee/(?P<app_id>\d+)/?$', 'app_fee', name='app_fee'),
    url(r'^/?$', 'apply', name='apply'),
)





