from itaco.models import Family, Profile, Student, SchoolYear, CommitteeJob, BoardPosition
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db.models import Q


# Create dicts separately for each roster, so we can re-use them in the print view.
# Just pass in printable = True and you get just the dict back, without the render_to_response.

def roster_families(request,printable=False):
    roster = Family.has_students.all() # Uses custom family manager in models.py
    cur_year = SchoolYear.objects.get(current=True)
    
    dict_families = {
        'roster': roster,
        'cur_year': cur_year,
        'type': "families",
        'title': "Family Roster"            
    }
    
    if printable:
        return dict_families
    else:
        return render_to_response('roster/roster.html', 
            dict_families,
            context_instance = RequestContext(request),
        )


def roster_parents(request,faces=None):
    roster = Profile.has_students.all() # Alpha ordering happens in the ProfileManager model, not here.
    cur_year = SchoolYear.objects.get(current=True)
    if faces:
        template = 'roster/roster_faces.html'
    else:
        template = 'roster/roster.html'
    return render_to_response(template, 
        {
            'roster': roster,
            'cur_year': cur_year,            
            'type': "parents",
            'title': "Parent Roster",
            'faces': faces
        },
        context_instance = RequestContext(request),
    )
        
def roster_students(request,printable=False):
    roster = Student.objects.filter(enrolled=True).order_by('last_name')
    cur_year = SchoolYear.objects.get(current=True)
    
    dict_students = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "students",
        'title': "Student Roster"                
    }
    
    # for r in roster:
    #     print r.family.id

    if printable:
        return dict_students
    else:
        return render_to_response('roster/roster.html', 
            dict_students,
            context_instance = RequestContext(request),
        )
    
    

def roster_students_kinder(request,printable=False):
    roster = Student.objects.filter(enrolled=True,expected_grad_yr__grad_class='kind').order_by('last_name')
    cur_year = SchoolYear.objects.get(current=True)
    dict_kind = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "kinder",
        'title': "Kindergarten Roster"                    
    }
    
    if printable:
        return dict_kind
    else:
        return render_to_response('roster/roster.html', 
            dict_kind,
            context_instance = RequestContext(request),
        )

def roster_students_1st(request,printable=False):
    roster = Student.objects.filter(enrolled=True,expected_grad_yr__grad_class='1st').order_by('last_name')
    cur_year = SchoolYear.objects.get(current=True)    
    dict_1st = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "1st",           
        'title': "1st Grade Roster"             
    }
    
    if printable:
        return dict_1st
    else:
        return render_to_response('roster/roster.html', 
            dict_1st,
            context_instance = RequestContext(request),
        )    
        
        

def roster_students_2nd(request,printable=False):
    roster = Student.objects.filter(enrolled=True,expected_grad_yr__grad_class='2nd').order_by('last_name')
    cur_year = SchoolYear.objects.get(current=True)    

    dict_2nd = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "2nd",   
        'title': "2nd Grade Roster"                     
    }
    
    if printable:
        return dict_2nd
    else:
        return render_to_response('roster/roster.html', 
            dict_2nd,
            context_instance = RequestContext(request),
        )        
    

def roster_students_3rd(request,printable=False):
    roster = Student.objects.filter(enrolled=True,expected_grad_yr__grad_class='3rd').order_by('last_name')
    cur_year = SchoolYear.objects.get(current=True)    

    dict_3rd = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "3rd",        
        'title': "3rd Grade Roster"                                     
    }
    
    if printable:
        return dict_3rd
    else:
        return render_to_response('roster/roster.html', 
            dict_3rd,
            context_instance = RequestContext(request),
        )
    
def roster_students_4th(request,printable=False):
    roster = Student.objects.filter(enrolled=True,expected_grad_yr__grad_class='4th').order_by('last_name')
    cur_year = SchoolYear.objects.get(current=True)    

    dict_4th = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "4th",            
        'title': "4th Grade Roster"                                 
    }
    
    if printable:
        return dict_4th
    else:
        return render_to_response('roster/roster.html', 
            dict_4th,
            context_instance = RequestContext(request),
        )
        
def roster_students_5th(request,printable=False):
    roster = Student.objects.filter(enrolled=True,expected_grad_yr__grad_class='5th').order_by('last_name')
    cur_year = SchoolYear.objects.get(current=True)    

    dict_5th = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "5th",         
        'title': "5th Grade Roster"                                    
    }
    
    if printable:
        return dict_5th
    else:
        return render_to_response('roster/roster.html', 
            dict_5th,
            context_instance = RequestContext(request),
        )
            
def roster_teachers(request,printable=False):
    roster = Profile.objects.filter(user__groups__in=(87,),user__is_active=True).order_by('user__last_name')
    aides = Profile.objects.filter(user__groups__in=(89,),user__is_active=True).order_by('user__last_name')    
    
    dict_teachers = {
        'roster': roster,
        'aides': aides,            
        'type': "teachers",        
        'title': "Teachers Roster"                                     
    }
    
    if printable:
         return dict_teachers
    else:
         return render_to_response('roster/roster_teachers.html', dict_teachers,
            context_instance = RequestContext(request),
    )  
    
    
def roster_participators(request,printable=False):
    roster = Profile.objects.filter(participating_parent=True,user__is_active=True).order_by('user__last_name')

    return render_to_response('roster/roster_participators.html', locals(),
    context_instance = RequestContext(request),
    )      
    
    
def roster_board(request,printable=False):
    # We include Teachers as a board position because committee jobs report to them so it makes
    # sense in the data model, but it's confusing to users and not "real" so we exclude it here.
    roster = BoardPosition.objects.all().exclude(title='teachers')
    cur_year = SchoolYear.objects.get(current=True)    
    
    dict_board = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "board",      
        'title': "Board Roster"                                       
    }

    if printable:
         return dict_board
    else:
         return render_to_response('roster/roster_board.html', dict_board,
            context_instance = RequestContext(request),
    ) 
    
    


def roster_jobs(request,printable=False):
    # roster = CommitteeJob.objects.all().order_by('title')
    
    # Only show jobs that have one or more occupying parents
    roster = CommitteeJob.objects.annotate(num_parents=Count('profile')).filter(num_parents__gte=1).order_by('title')
    
    # for pos in roster2:
    #     print pos.profile_set.all().count()
    
    dict_jobs = {
        'roster': roster,
        'type': "jobs",      
        'title': "Committee Jobs (Family Jobs)"                                       
    }

    if printable:
         return dict_jobs
    else:
         return render_to_response('roster/roster_jobs.html', dict_jobs,
            context_instance = RequestContext(request),
    )   

def roster_jobs_detail(request,jobid=None):
    '''
    Detailed description of a family job
    '''
    job = get_object_or_404(CommitteeJob,id=jobid)

    return render_to_response('roster/roster_jobs_detail.html', locals(),
        context_instance = RequestContext(request),
    )   

def roster_jobs_all(request):
    '''
    Complete list of family jobs, whether they're currently occupied or not
    '''
    jobs = CommitteeJob.objects.all()

    return render_to_response('roster/roster_jobs_all.html', locals(),
        context_instance = RequestContext(request),
    )  


def roster_print(request):
    """
    Re-use all of the roster dictionaries from functions above in one giant print-friendly view
    """
    printable = True
    cur_year = SchoolYear.objects.get(current=True)    
    roster_fam = roster_families(request,printable)
    roster_teach = roster_teachers(request,printable)
    roster_brd = roster_board(request,printable)   
    roster_famjobs = roster_jobs(request,printable)
    roster_kind = roster_students_kinder(request,printable) 
    roster_1 = roster_students_1st(request,printable)            
    roster_2 = roster_students_2nd(request,printable)            
    roster_3 = roster_students_3rd(request,printable)            
    roster_4 = roster_students_4th(request,printable)            
    roster_5 = roster_students_5th(request,printable)                            
    

    return render_to_response('roster/roster_print.html', 
        {
            'cur_year':cur_year,
            'roster_fam':roster_fam,
            'roster_teach':roster_teach,       
            'roster_brd':roster_brd,     
            'roster_famjobs':roster_famjobs, 
            'roster_kind':roster_kind,    
            'roster_1':roster_1,
            'roster_2':roster_2,
            'roster_3':roster_3,
            'roster_4':roster_4,
            'roster_5':roster_5,                                                
        },
        context_instance = RequestContext(request),
    )


def roster_export(request):
    ''' Provide various export options (print, vcard)'''
    
    return render_to_response('roster/export.html', locals(),
        context_instance = RequestContext(request),
    ) 
    

    
def roster_search(request):
    """
    Search in rosters by name or content in About field.
    """

    if request.GET:    

        query_string = ''
        found_profiles = None
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            found_profiles = Profile.objects.filter(
                Q(about__icontains=query_string) |
                Q(tags__icontains=query_string) |                
                Q(user__first_name__icontains=query_string) |
                Q(user__last_name__icontains=query_string)                 
            )

    else :
        query_string = None
        found_profiles = None
        
    # print found_profiles

    return render_to_response('roster/search.html',
      { 'query_string': query_string, 'found_profiles': found_profiles },
      context_instance=RequestContext(request))


    
    
def vcard_single(request, username):
    """
    View function for returning one vcard
    """

    person = Profile.objects.get(user__username=username)

    response = render_to_response("roster/vcard.txt", {'p':person},)    
    filename = "%s%s.vcf" % (person.user.first_name, person.user.last_name)
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'text/x-vCard; charset=utf-8'    
    return response
    
    
def vcard_multi(request):
    """
    View function for returning multiple vcards
    """

    people = Profile.objects.all()

    response = render_to_response("roster/vcard_multi.txt", {'people':people},)    
    filename = "crestmont_multi.vcf"
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'text/x-vCard; charset=utf-8'    
    return response    
        
        
def signin_print(request):
    '''
    Printable sign-in / sign-out sheet
    '''
    
    # We don't necessarily have a primary contact for each family, 
    # so we'll need a custom list with lots of logic, not a simple queryset.

    students = []
    for s in Student.objects.filter(enrolled=True).order_by('last_name'):
        try:
            # This will be true when the student has exactly one parent marked as primary contact
            primary = Profile.objects.select_related().get(family=s.family,primary_contact=True)
            
        except:
            # Otherwise we'll pick the first parent in the query
            primary = Profile.objects.select_related().filter(family=s.family)[:0]

        # The secondary contact will be the 2nd in the query not marked primary
        secondary = Profile.objects.select_related().filter(family=s.family,primary_contact=False)
        
    
        # Append this info the students list
        students.append({'student':s,'primary':primary,'secondary':secondary})


    return render_to_response('roster/signin_print.html', 
        locals(),
        context_instance = RequestContext(request),
    )        
        
