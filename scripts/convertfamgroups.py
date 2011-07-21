"""
First gen of site treated families as subclass of Group model. 
Then we converted to freestanding Family model. This script copied the 
old group name into the new Family 'name' field.
"""

#################### Set up Django environment

import os, sys, site

site.addsitedir('/home/crest/sites/crest/lib/python2.5/site-packages')

# Toggle/comment these depending on whether you're testing in dev or running in production.
sys.path.append('/home/crest/sites/crest')
sys.path.append('/home/crest/sites/crest/ourcrestmont')
# sys.path.append('/Users/shacker/Sites/virtualenvs/crestmontschool.org')
# sys.path.append('/Users/shacker/Sites/virtualenvs/crestmontschool.org/ourcrestmont')



os.environ['DJANGO_SETTINGS_MODULE'] ='ourcrestmont.settings'

from django.core.management import setup_environ
from ourcrestmont import settings
# import settings
setup_environ(settings)



#################### Import models from Django project and custom vars

from ourcrestmont.itaco.models import *
from django.contrib.auth.models import User, Group

#################### Start work

groups = Group.objects.all()

for g in groups:
    print g.name
    try:
        f = Family.objects.get(id=g.id)
        f.famname = g.name
        f.save()
    except:
        pass
    