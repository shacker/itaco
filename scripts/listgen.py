"""
Python replacement for old listgen.sh script (or at least half of it). 
Extract lists of email addresses per Group and write them to text files.
listgen.sh will call this script and do the subsequent mailman subscription magic.
 
"""

#################### Set up Django environment

import os, sys, site

site.addsitedir('/home/crest/sites/crest/lib/python2.7/site-packages')

# Toggle/comment these depending on whether you're testing in dev or running in production.
sys.path.append('/home/crest/sites/crest')
sys.path.append('/home/crest/sites/crest/crest')
# sys.path.append('/Users/shacker/Sites/virtualenvs/crestmontschool.org')
# sys.path.append('/Users/shacker/Sites/virtualenvs/crestmontschool.org/ourcrestmont')



os.environ['DJANGO_SETTINGS_MODULE'] ='crest.settings'

from django.core.management import setup_environ
from ourcrestmont import settings
setup_environ(settings)

# Folder to store output lists before adding to Mailman
filepath = os.path.join(os.path.basename(__file__), 'scripts','listgen')


#################### Import models from Django project and custom vars

from ourcrestmont.itaco.models import *
from django.contrib.auth.models import User, Group
from django.db.models import Q

#################### Start work

# print "output path is:"
# print settings.LISTGENPATH

def write_file(group,peeps=None):    
    # Re-usable function to write membership text files that feed mailing lists 
    # 1) Store regular subscribers
    # 2) Add any extras to the same list
    # 3) Create a second nomail list for the same group
        
    # Open a file for the current group
    thefile = open(os.path.join(settings.LISTGENPATH, group.list + ".txt"), 'w')

    if peeps:
        for p in peeps :
            # thefile.write("%s %s <%s> \n" % (p.user.last_name, p.user.first_name, p.user.email))
            thefile.write("%s \n" % (p.user.email))

    if extra:
        thefile.write(extra)          

    thefile.close()



# Generate lists for each set in ListExtra. Limit all selections to active users!
# For each, see if there are "list extras" to append to the membership list.

groupset = ListExtra.objects.all()

for group in groupset :
    # Reset peeps so it doesn't carry over from previous iteration
    peeps = None

    if group.list == 'kindergarten' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='kind',user__is_active=True)
        
    if group.list == 'first' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='1st',user__is_active=True)

    if group.list == 'second' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='2nd',user__is_active=True)
                
    if group.list == 'third' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='3rd',user__is_active=True)    
                        
    if group.list == 'fourth' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='4th',user__is_active=True)   
        
    if group.list == 'fifth' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='5th',user__is_active=True)  
        
    if group.list == 'board' :
        # Be sure to exclude teachers from the board list - they show up there because iTaco 
        # makes teachers into board members for reporting-to purposes, but that's not acceptable here.
        peeps = Profile.objects.filter(board_pos__in=BoardPosition.objects.all()).exclude(user__groups__in=(87,))
        
    if group.list == 'teachers' :
        peeps = Profile.objects.filter(user__groups__in=(87,),user__is_active=True)
        
    if group.list == 'alumni' :
        # For alumni we need both a query - to get all parents of alumni, AND the extralist - to deal with the legacy alumni who were never in itaco.
        # Note that parents go on the alumni list as soon as they have one student who has graduated, even if another is still enrolled.
        peeps = Profile.objects.filter(family__student__alumni=True,)
        
    if group.list == 'executivecom' :
        # For executivecom we need the group iterator, but no query - we'll just use extralist for them
        peeps = None
        
    if group.list == 'alphageeks' :
        # For executivecom we need the group iterator, but no query - we'll just use extralist for them
        peeps = None        
        
    if group.list == 'participation' :
        peeps = Profile.objects.filter(family__student__enrolled=True,participating_parent=True,user__is_active=True)          
                        
    if group.list == 'everyone' :
        
        # Everyone is defined as all parents in families that have one or more students enrolled, plus all teachers. Anyone else?
        peeps = Profile.objects.filter(
            Q(family__student__enrolled=True,user__is_active=True) | 
            Q(user__groups__in=(87,),user__is_active=True)
        )        
        
    # Combined queries for the mixed lists via Q objects:
    # http://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
    if group.list == 'twothree' :        
        peeps = Profile.objects.filter(
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='2nd',user__is_active=True) | 
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='3rd',user__is_active=True)
        )
        
    if group.list == 'fourfive' :        
        peeps = Profile.objects.filter(
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='4th',user__is_active=True) | 
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='5th',user__is_active=True)
        )
        
    # Some people opt to not receive any mail from crestmont lists. 
    # Respect the "no_lists" flag on the Profile model.
    try:
        peeps = peeps.exclude(no_lists=True)
    except:
        pass
                          
    #########
    # Now get any "extras" for the list (this handles the nomail people too)
    try:
        profiles = Profile.objects.filter(list_extras=group)
        extra = ''
        for p in profiles:
            # extra += "%s %s <%s>\n" % (p.user.last_name, p.user.first_name, p.user.email)
            extra += "%s\n" % (p.user.email)
    
    except:
        extra = None

    # Also add in the GMail archives and other misc extras
    if group.list == 'kindergarten':
        extra += 'crestmont.k@gmail.com\n'

    if group.list == 'first':
        extra += 'crestmont.1@gmail.com\n'

    if group.list == 'second':
        extra += 'crestmont.2@gmail.com\n'

    if group.list == 'third':
        extra += 'crestmont.3@gmail.com\n'

    if group.list == 'fourth':
        extra += 'crestmont.4@gmail.com\n'

    if group.list == 'fifth':
        extra += 'crestmont.5@gmail.com\n'


    # Handle the pre-iTaco alumni who don't have User objects in the system - stored in a permanent text file
    if group.list == 'alumni':
        alumpath = os.path.join(sys.path[0],'listgen-alumni.txt')
        extra += open(alumpath, 'r').read()
        


    # Commit!
    write_file(group,peeps)
    



