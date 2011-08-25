"""
Python replacement for old listgen.sh script (or at least half of it). 
Extract lists of email addresses per Group and write them to text files.
listgen.sh will call this script and do the subsequent mailman subscription magic.
 
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

# Folder to store output lists before adding to Mailman
filepath = os.path.join(os.path.basename(__file__), 'scripts','listgen'),


#################### Import models from Django project and custom vars

from ourcrestmont.itaco.models import *
from django.contrib.auth.models import User, Group
from django.db.models import Q

#################### Start work

print "output path is:"
print settings.LISTGENPATH

def write_file(group,peeps=None,extra=None,extranomail=None):
    # Re-usable function to write text files. 
    
    thefile = open(os.path.join(settings.LISTGENPATH, group + ".txt"), 'w')
    
    if peeps:
        for p in peeps :
            # Most queries give us Profile objects, but some (teahers) give us User objects.
            # But in all cases we want the User object when writing the email addr
            # try :
            #     p = p.user
            # except:
            #     # p is still p
            #     p = p
            thefile.write("%s <%s> \n" % (p, p.user.email))
            
    try:
        if extra:
            thefile.write(extra)            
    except:
        pass
        
    # Close file for writing
    # There's prob a better way to do this than closing and re-opening but this works.
    thefile.close()
    
    # Make a temp file, remove duplicate lines, strip out blanks
    tempfile = open(os.path.join(settings.LISTGENPATH, group + ".txt"), 'r')
    lines = []
    for line in tempfile:
        lines.append(line.strip())
    # Remove duplicates with the set() function
    lines = set(lines)
    
    # Re-open the original file for writing and replace its contents
    thefile = open(os.path.join(settings.LISTGENPATH, group + ".txt"), 'w')
    for line in lines:
        thefile.write(line  + "\n")

    # Close file for writing again.
    thefile.close()    
        
    print "Generated list for %s" % group
    
    # Now process the -nomail extras, if they exist
    if extranomail :
        thefilenomail = open(os.path.join(settings.LISTGENPATH, group + "-nomail.txt"), 'w')
        thefilenomail.write(extranomail)
        thefilenomail.close
        print "Generated NOMAIL list for %s" % group

    ### End file generation ###



# Generate lists for the following. Limit all selections to active users!
# For each, see if there are "list extras" to append to the membership list
groupset = ['kindergarten','first','second','third','twothree','fourth','fifth','fourfive','board','teachers','alumni','executivecom','participation','everyone',]

for group in groupset :

    if group == 'kindergarten' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='kind',user__is_active=True)
        
    if group == 'first' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='1st',user__is_active=True)

    if group == 'second' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='2nd',user__is_active=True)
                
    if group == 'third' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='3rd',user__is_active=True)    
                        
    if group == 'fourth' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='4th',user__is_active=True)   
        
    if group == 'fifth' :
        peeps = Profile.objects.filter(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='5th',user__is_active=True)  
        
    if group == 'board' :
        # Be sure to exclude teachers from the board list - they show up there because iTaco 
        # makes teachers into board members for reporting-to purposes, but that's not acceptable here.
        peeps = Profile.objects.filter(board_pos__in=BoardPosition.objects.all()).exclude(user__groups__in=(87,))
            
    if group == 'teachers' :
        peeps = Profile.objects.filter(user__groups__in=(87,),user__is_active=True)
        
    if group == 'alumni' :
        # For alumni we need both a query - to get all parents of alumni, AND the extralist - to deal with the legacy alumni who were never in itaco.
        # Note that parents go on the alumni list as soon as they have one student who has graduated, even if another is still enrolled.
        # peeps = None 
        peeps = Profile.objects.filter(family__student__alumni=True,)
        
        
    if group == 'executivecom' :
        # For executivecom we need the group iterator, but no query - we'll just use extralist for them
        peeps = None
        
    if group == 'participation' :
        peeps = Profile.objects.filter(family__student__enrolled=True,participating_parent=True,user__is_active=True)          
                        
    if group == 'everyone' :
        
        # Everyone is defined as all parents in families that have one or more students enrolled, plus all teachers. Anyone else?
        peeps = Profile.objects.filter(
            Q(family__student__enrolled=True,user__is_active=True) | 
            Q(user__groups__in=(87,),user__is_active=True)
        )        
        
    # Combined queries for the mixed lists via Q objects:
    # http://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects
    if group == 'twothree' :        
        peeps = Profile.objects.filter(
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='2nd',user__is_active=True) | 
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='3rd',user__is_active=True)
        )
        
    if group == 'fourfive' :        
        peeps = Profile.objects.filter(
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='4th',user__is_active=True) | 
            Q(family__student__enrolled=True,family__student__expected_grad_yr__grad_class='5th',user__is_active=True)
        )
        
    # Some people opt to not receive any mail from crestmont lists. Respect the "no_lists" flag on the Profile model.
    try:
        peeps = peeps.exclude(no_lists=True)
    except:
        pass
                          
    #########
    # Now get any regular "extras" for the list 
    try:
        mlist = ListExtra.objects.get(list=group)
        profiles = Profile.objects.filter(list_extras=mlist)
        # Convert the set of profiles into a string of email addresses, one per line
        extra = ''
        for p in profiles:
            extra += "%s <%s>\n" % (p, p.user.email)

    except:
        extra = None


    # Now get any "nomail" extras for the list 
    try:

        extranomailstring = "%s-nomail" % group
        mlist = ListExtra.objects.get(list=extranomailstring)
        profiles = Profile.objects.filter(list_extras=mlist)
        # Convert the set of profiles into a string of email addresses, one per line
        extranomail = ''
        for p in profiles:
            extranomail += "%s <%s>\n" % (p, p.user.email)
        
    except:
        extranomail = None
    
    # print extranomail
    

    ####### Commit!
    write_file(group,peeps,extra,extranomail)
    



