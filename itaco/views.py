from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from ourcrestmont.itaco.models import *
from ourcrestmont.itaco.constants import *
from ourcrestmont.itaco.forms import ChargeForm, PartCredForm, MaintOblForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test

# For reading files from listen output
import sys,os

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
        return render_to_response('roster.html', 
            dict_families,
            context_instance = RequestContext(request),
        )


def roster_parents(request):
    roster = Parent.has_students.all() # Alpha ordering happens in the ParentManager model, not here.
    cur_year = SchoolYear.objects.get(current=True)
    return render_to_response('roster.html', 
        {
            'roster': roster,
            'cur_year': cur_year,            
            'type': "parents",
            'title': "Parent Roster"
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

    if printable:
        return dict_students
    else:
        return render_to_response('roster.html', 
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
        return render_to_response('roster.html', 
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
        return render_to_response('roster.html', 
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
        return render_to_response('roster.html', 
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
        return render_to_response('roster.html', 
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
        return render_to_response('roster.html', 
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
        return render_to_response('roster.html', 
            dict_5th,
            context_instance = RequestContext(request),
        )
            
def roster_teachers(request,printable=False):
    roster = Parent.objects.filter(user__groups__in=(87,),user__is_active=True).order_by('user__last_name')
    aides = Parent.objects.filter(user__groups__in=(89,),user__is_active=True).order_by('user__last_name')    
    
    dict_teachers = {
        'roster': roster,
        'aides': aides,            
        'type': "teachers",        
        'title': "Teachers Roster"                                     
    }
    
    if printable:
         return dict_teachers
    else:
         return render_to_response('roster_teachers.html', dict_teachers,
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
         return render_to_response('roster_board.html', dict_board,
            context_instance = RequestContext(request),
    ) 
    
    


def roster_jobs(request,printable=False):
    roster = CommitteeJob.objects.all().order_by('title')
    cur_year = SchoolYear.objects.get(current=True)    
    
    dict_jobs = {
        'roster': roster,
        'cur_year': cur_year,            
        'type': "jobs",      
        'title': "Committee Jobs (Family Jobs)"                                       
    }

    if printable:
         return dict_jobs
    else:
         return render_to_response('roster_jobs.html', dict_jobs,
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
    

    return render_to_response('roster_print.html', 
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


def listgen(request):
    """
    Listgen script runs externally, via cronjob, and generates text files. This just lets people see who's on the lists.
    """
    # Populate a dictionary mldict with lists for values, like:
    # {kindergarten:[foo,bar],first:[baz,blob]}
    
    mldict = {}
    nomailmldict = {}
    groupset = ['kindergarten','first','second','third','twothree','fourth','fifth','fourfive','board','teachers','alumni','executivecom','participation','everyone',]
    for group in groupset :
        try: # Get the regular members
            tempfile = open(os.path.join(settings.LISTGENPATH, group + ".txt"), 'r')                    
            mldict[group] = tempfile.readlines()
        except:
            pass
        
        try: # Get the nomail members
            nomailtempfile = open(os.path.join(settings.LISTGENPATH, group + "-nomail.txt"), 'r')                    
            nomailmldict[group] = nomailtempfile.readlines()
        except:
            pass            
            
    return render_to_response('tools/listgen.html',  locals(), context_instance = RequestContext(request),)    



def family_contact(request,fam_id):
    """
    Get base objects for family, and for parents and students in this family.
    """
    f = get_object_or_404(Family,pk=fam_id)
    p = Parent.objects.filter(family=fam_id)
    s = Student.objects.filter(family=fam_id)
    
    # Only superusers and the current family can view their own finance details.
    if request.user.is_superuser:
        canview_charges = 1
    else:
        canview_charges = 0

    return render_to_response('family-contact.html', 
        {
            'family': f,
            'parents': p,            
            'students': s, 
            'canview_charges': canview_charges,
        },
        context_instance = RequestContext(request),
    )


 
def family_detail(request,fam_id,csv = False,year='',period='',all=''):
    
    """
    Start/end dates for slice of the data we're currently viewing. 
    From the URL we get "year" or "period" or none.
    None is the default and shows the current school year.
    
    All obligations are annual, but it's possible to view this page 
    either by year or by billing period. Therefore we need a separate
    start/stop date for the period when calculating obligations (the
    period is always one year as far as obligations are concerned). 
    Otherwise the user would see a slice of fulfilled obligations
    limited to the duration of one billing period, which would be confusing.
    """
    
    if year :
        # print "year"
        period = SchoolYear.objects.get(pk=year)
        period_period = False # Need to send a custom var to template for fancy string formatting        
        period_string = "School Year %s" % period.title
        period_start = period.start
        period_end = period.end
        obl_period_start = period_start
        obl_period_end = period_end
        
    
    elif period : 
        # print "period"
        period = BillingPeriod.objects.get(pk=period)
        period_period = True 
        period_string = "Billing Period: "
        period_start = period.start
        period_end = period.end
        
        # Here's the exception for obligation start/end dates.
        # From the SchoolYear table, find the school year that this billing period falls inside of.
        obl_period_year = SchoolYear.objects.get(start__lte=period.start,end__gte=period.end)
        obl_period_start = obl_period_year.start
        obl_period_end = obl_period_year.end
        
        
    elif all : 
        # print "all"
        period_string = "All Billing Periods. Ever."
        period_period = False # Need to send a custom var to template for string fancy string formatting        
        # Fake this by setting start and end points in distant past and distant future
        period_start = '1960-01-01'
        period_end = '3000-12-12'
        obl_period_start = period_start
        obl_period_end = period_end        

        
    else :  # Assume current year for the view
        # print "else"
        period = SchoolYear.objects.get(current=True) 
        period_period = False # Need to send a custom var to template for fancy string formatting                
        period_string = "School Year %s" % period.title
        period_start = period.start
        period_end = period.end
        obl_period_start = period_start
        obl_period_end = period_end        
        
    # print period_period
    # print period_string
    # print period
    # print year

    """
    Now we can get actual start and stop dates for the current period view.
    All queries below are filtered by greater than / less than these:
    
    date__gte=period_start,date__lte=period_end
    """


    """
    Get base objects for family, and for parents and students in this family.
    """
    f = get_object_or_404(Family,pk=fam_id)
    p = Parent.objects.filter(family=fam_id)
    s = Student.objects.filter(family=fam_id)

    """
    Obligation constants brought in from settings file
    """
    obl_maint_hours_due = settings.ANN_MAINTENANCE_HOURS # This gets adjusted later; 7 hours if family has board position; 4 hours if that position is shared.
    obl_member_meetings_due = settings.ANN_MEMBER_MEETINGS
    obl_fundraising_hours_due = settings.ANN_EXTERNAL_FUNDRAISING_HOURS
    obl_housekeeping_due = settings.ANN_HOUSEKEEPING_SESSIONS
    obl_field_trips_due = settings.ANN_FIELD_TRIPS
    obl_coop_jobs_due = settings.ANN_COOP_JOBS

    """
    Annual obligation depends on number of kids in family, which we have via s.count()
    """
    num_kids = s.count()
    if num_kids > 1 :
        obl_annual_obligation_due = settings.ANN_OBLIGATION_2_CHILD
    else: 
        obl_annual_obligation_due = settings.ANN_OBLIGATION_1_CHILD
            
    """
    This family may hold one or more board positions. Get list of all positions 
    occupied by this family. For each in list, determine whether other members
    in the school occupy the same position. If so, split the credit by that 
    number of people. 
    
    Also adjust the number of maintenance obligation hours depending on whether a
    board position is occupied, and whether that board position is shared.
    """
    board_positions = BoardPosition.objects.filter(parent__in=p)
    board_string = ""
    board_credit = 0
    for b in board_positions:
        # Does anyone else occupy this position? Get number of people who have same pos.
        num_other_occupied = len(Parent.objects.filter(board_pos=b.id))
        board_string += "%s ($%d)<br />" % (b, b.credit)
        
        if num_other_occupied > 1 :
            adj_credit = b.credit / num_other_occupied
            board_string += "This position is shared by %d people, including you. Adjusted credit: $%d<br /><br />" % (num_other_occupied, adj_credit)
            board_credit += adj_credit
            obl_maint_hours_due = settings.ANN_MAINTENANCE_HOURS_BOARD_SHARED # Adjust maint hours obligation if family occupies a shared board position
        else :
            board_string += "Credit: $%d<br />" % (b.credit)
            board_credit += b.credit
            obl_maint_hours_due = settings.ANN_MAINTENANCE_HOURS_BOARD # Adjust maint hours obligation if family occupies a solo board position
    
    
    """All charges and credits filtered by period start and period end"""
    
    cr = Credit.objects.filter(
        family=fam_id,
        date__gte=period_start,
        date__lte=period_end,
        ).order_by('-date',)
    
    o = Obligation.objects.filter(
        family=fam_id,
        date__gte=obl_period_start,
        date__lte=obl_period_end,
        ).order_by('-date',)
    
    ch = Charge.objects.filter(
        family=fam_id,
        date__gte=period_start,
        date__lte=period_end,
        ).order_by('-date',)
    
    # In models.py we break out all charge types that are not hourly regular daycare as a tuple of tuples.
    # Here we need to get those into a list, so loop through, getting the first value (like "msc") append to list.
    # Then pass that list into the query below. 
    # charge_other_types = []
    # for c in CHARGE_TYPE_CHOICES :
    #     print c[0]
    #     charge_other_types.append(c[0])
    #     
    # ch_other = Charge.objects.filter(
    #     family=fam_id,
    #     date__gte=period_start,
    #     date__lte=period_end,
    #     type__in=(charge_other_types), # Filter in the other type charges 
    #     ).order_by('-date',)


        # ch_other = Charge.objects.filter(
        #     family=fam_id,
        #     date__gte=period_start,
        #     date__lte=period_end,
        #     type__in=('mshc','mmh','mfr','adj','edc1','edc2','edc3','dclpu',), # Filter in the other type charges 
        #     ).order_by('-date',)
                    

    # Need a list of years and a list of billing periods to send to the template for selector picklists
    year_list = SchoolYear.objects.all()
    bp_list = BillingPeriod.objects.all().order_by('-start')
    
            
    # Only staff/superuser and the current family can view their own finance details.
    # Since we only need to block from view part of the data in the family-details template,
    # send canview_charges to the template.
    
    # First obtain the current user's family ID
    try:
        p=Parent.objects.get(user=request.user.id)
        myfam_id=p.family.id
    except:
        myfam_id=None
        
    
    if request.user.is_staff:
        canview_charges = 1
    elif myfam_id == f.id : # Uses fam_id from context processor.
        canview_charges = 1
    else:
        canview_charges = 0        

    # print myfam_id
    # print fam_id
    # print f.id
    # print canview_charges    
    


    """
    Calculate totals. Blank everything out first. 
    """
    # total_chargedaycare_hours = total_chargedaycare_dollars = 0
    # total_chargedaycare_hours = ch_daycare.aggregate(Sum('amount'))['amount__sum']
    # total_chargedaycare_dollars = ch_daycare.aggregate(Sum('charged_amount'))['charged_amount__sum']
    # total_chargeother_dollars = ch_other.aggregate(Sum('charged_amount'))['charged_amount__sum']  
    
    total_charge_dollars = ch.aggregate(Sum('charged_amount'))['charged_amount__sum']        

    if total_charge_dollars == None: # Can't test for None in template, but can compare to zero; convert
        total_charge_dollars = 0
    
    # if total_chargeother_dollars == None: # Can't test for None in template, but can compare to zero; convert
    #     total_chargeother_dollars = 0        

    total_credit_hours = total_credit_dollars = total_credit_units = 0
    total_credits = cr.aggregate(Sum('charged_amount'))['charged_amount__sum']

    total_obligation_hours = total_obligation_dollars = total_obligation_units = 0        

        
    """
    Obligation totals per unit type
    """
    obl_hr_list = o.filter(units='hours',)
    for i in obl_hr_list:
        total_obligation_hours = total_obligation_hours + i.amount

    obl_dl_list = o.filter(units='dollars',)
    for i in obl_dl_list:
        total_obligation_dollars = total_obligation_dollars + i.amount

    obl_ut_list = o.filter(units='units',)
    for i in obl_ut_list:
        total_obligation_units = total_obligation_units + i.amount

        
    """
    Completed obligations per obligation type
    Using Django's Aggregate functions in v1.1
    http://docs.djangoproject.com/en/dev/topics/db/aggregation/
    Aggregate returns a dictionary - we retrieve the dictionary value we need, 
    which is always amount__sum.
    """
    obl_member_meetings_complete = o.filter(type='mbsmtg').aggregate(Sum('amount'))['amount__sum']
    obl_maint_hours_complete = o.filter(type='maint').aggregate(Sum('amount'))['amount__sum']
    obl_fundraising_hours_complete = o.filter(type='fundrais').aggregate(Sum('amount'))['amount__sum']
    obl_field_trips_complete = o.filter(type='fldtrp').aggregate(Sum('amount'))['amount__sum']
    obl_housekeeping_complete = o.filter(type='housekpg').aggregate(Sum('amount'))['amount__sum']
    obl_coop_jobs_complete = o.filter(type='cmt_coop').aggregate(Sum('amount'))['amount__sum']
    
    # Annual obligation depends on number of kids in family, which we have via s.count()
    num_kids = s.count()
    if num_kids > 1 :
        obl_annual_obligation_complete = o.filter(type='oblscrp1').aggregate(Sum('amount'))['amount__sum']
    else :
        obl_annual_obligation_complete = o.filter(type='oblscrp2').aggregate(Sum('amount'))['amount__sum']
    
    """
    Queries for completed obligations done. Change None to 0 as needed to avoid "None divided by 0" errors.
    """
    if obl_member_meetings_complete == None : obl_member_meetings_complete = 0
    if obl_maint_hours_complete == None : obl_maint_hours_complete = 0
    if obl_fundraising_hours_complete == None : obl_fundraising_hours_complete = 0
    if obl_field_trips_complete == None : obl_field_trips_complete = 0
    if obl_housekeeping_complete == None : obl_housekeeping_complete = 0
    if obl_coop_jobs_complete == None : obl_coop_jobs_complete = 0
    if obl_annual_obligation_complete == None : obl_annual_obligation_complete = 0

    # Make family_dict a global so we can use it both in this function and in render_to_csv
    global family_dict
        

    """
    Build this dictionary of data outside of render_to_response()
    so it can be shared with the csv generator.
    """
    family_dict = {
    
          # General
          'family': f,
          'parents': p,
          'students': s, 
          'year_list': year_list, # List of years
          'bp_list': bp_list,   # List of billing periods
          'num_kids': num_kids,
          'canview_charges': canview_charges,
   
          
          # Period
          'period': period,
          'period_period': period_period,
          'period_string': period_string,
          
          # Obligations
          'obl_hr_list': obl_hr_list,
          'obl_dl_list': obl_dl_list,
          'obl_ut_list': obl_ut_list,                    
          'obl_member_meetings_due' : obl_member_meetings_due,
          'obl_maint_hours_due' : obl_maint_hours_due,
          'obl_fundraising_hours_due' : obl_fundraising_hours_due,
          'obl_housekeeping_due' : obl_housekeeping_due,
          'obl_field_trips_due' : obl_field_trips_due,
          'obl_coop_jobs_due' : obl_coop_jobs_due,
          'obl_annual_obligation_due' : obl_annual_obligation_due,

          # Charges
          'charges': ch,
          # 'charges_daycare': ch_daycare,  
          'daycare_hourly_rate': settings.DAYCARE_REGULAR_HOURLY,
          # 'total_chargedaycare_hours': total_chargedaycare_hours,
          # 'total_chargedaycare_dollars': total_chargedaycare_dollars,
          # 'charges_other': ch_other,            
          # 'total_chargeother_dollars': total_chargeother_dollars,
          'total_charge_dollars': total_charge_dollars,          

          # Credits
          'credits': cr,   
          'total_credits':total_credits,
          'board_credit': board_credit,
          'board_string': board_string,          
                    
          # Obligations
          'obligations': o,              
          'total_obligation_hours': total_obligation_hours,
          'total_obligation_dollars': total_obligation_dollars,
          'total_obligation_units': total_obligation_units,
          'obl_maint_hours_complete' : obl_maint_hours_complete,
          'obl_member_meetings_complete' : obl_member_meetings_complete,
          'obl_fundraising_hours_complete' : obl_fundraising_hours_complete,
          'obl_housekeeping_complete' : obl_housekeeping_complete,                             
          'obl_field_trips_complete' : obl_field_trips_complete,                             
          'obl_coop_jobs_complete' : obl_coop_jobs_complete,   
          'obl_annual_obligation_complete' : obl_annual_obligation_complete,             

          
          # Chart data
          # +.0001 compensates for a bug in django-googlecharts - without it pie chart collapses.
          'maint_hours_data' : [obl_maint_hours_complete + .0001, obl_maint_hours_due - obl_maint_hours_complete],
          'member_meetings_data' : [obl_member_meetings_complete + .0001, obl_member_meetings_due - obl_member_meetings_complete],
          'fundraising_data' : [obl_fundraising_hours_complete + .0001, obl_fundraising_hours_due - obl_fundraising_hours_complete],
          'housekeeping_data' : [obl_housekeeping_complete + .0001, obl_housekeeping_due - obl_housekeeping_complete],
          'field_trips_data' : [obl_field_trips_complete + .0001, obl_field_trips_due - obl_field_trips_complete],
          'coop_jobs_data' : [obl_coop_jobs_complete + .0001, obl_coop_jobs_due - obl_coop_jobs_complete],
          'annual_obligation_data' : [obl_annual_obligation_complete + .0001, obl_annual_obligation_due - obl_annual_obligation_complete],    
          
          'thepath': request.path,
        
      }
      
    
    """
    If CSV was passed to this function as True, return output of render_to_csv() 
    for this family. Otherwise return normal HTML.
    """
    if csv:
        return render_to_csv(request, fam=fam_id)
    else:
        # Send query result objects to template
        return render_to_response('family.html', 
            family_dict,
            context_instance = RequestContext(request),
        )  
    


def render_to_csv(request,fam):
    """
    Output data from view above as CSV.
    """
    response = render_to_response("family-tables.html", family_dict,)    
    filename = "family-data.xls" 
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
    return response
    

# View restricted to users with is_staff permissions    
@user_passes_test(lambda u: u.is_staff, login_url='/')
def batch_daycare_charges(request):
    """
    Provides ability to add multiple daycare charges at once. 
    For privileged users (Trackers) only.
    """

    DaycareChargeFormSet = formset_factory(ChargeForm, extra=20)
    if request.method == 'POST':
        formset = DaycareChargeFormSet(request.POST, request.FILES)
        
        if formset.is_valid():
            for form in formset.cleaned_data:
                """
                This shouldn't be necessary - cleaned_data should not pass in empty dictionaries.
                But we're getting them anyway if no data is entered into one of the forms. 
                So we manually skip processing of empty dicts with "if form: "
                """

                if form:
                    charge = Charge()
                    charge.family = form['family']
                    charge.type = 'hrdc'
                    charge.date = request.POST['the_date']          
                    charge.amount = form['amount']
                    charge.note = form['note']
                    charge.save()
                
                    request.user.message_set.create(message="%s daycare hours added for %s" % (form['amount'], form['family']))
        
        else:
            request.user.message_set.create(message="Something went wrong. No charges have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")
        
        # Redirect to a new page to avoid possibility of a browser reload re-adding charges.
        return HttpResponseRedirect("complete")
    else:
        formset = DaycareChargeFormSet()

    return render_to_response(
        'tools/charge_batch.html', 
        {'formset': formset},
        context_instance = RequestContext(request),
        )
    

def batch_daycare_charges_complete(request):
    """
    Page to display after batch daycare charges have been added.
    """
    return render_to_response(
        'tools/charge_batch_complete.html', 
        context_instance = RequestContext(request),
        )




# View restricted to users with is_staff permissions    
@user_passes_test(lambda u: u.is_staff, login_url='/')
def batch_maintenance_obl(request):
    """
    Provides ability to add multiple maintenance obligations at once. 
    For privileged users (Trackers) only.
    """

    MaintOblFormSet = formset_factory(MaintOblForm, extra=20)
    if request.method == 'POST':
        formset = MaintOblFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset.cleaned_data:
                """
                This shouldn't be necessary - cleaned_data should not pass in empty dictionaries.
                But we're getting them anyway if no data is entered into one of the forms. 
                So we manually skip processing of empty dicts with "if form: "
                """

                if form:
                    obl = Obligation()
                    obl.family = form['family']
                    obl.type = 'maint'
                    obl.date = request.POST['the_date']          
                    obl.amount = form['amount']
                    obl.note = form['note']
                    # obl.units = 'hours'                    
                    obl.save()

                    request.user.message_set.create(message="%s maintenance hours added for %s" % (form['amount'], form['family']))

        else:
            request.user.message_set.create(message="Something went wrong. No obligation hours have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")

        # Redirect to a new page to avoid possibility of a browser reload re-adding charges.
        return HttpResponseRedirect("complete")
    else:
        formset = MaintOblFormSet()

    return render_to_response(
        'tools/maint_obl_batch.html', 
        {'formset': formset},
        context_instance = RequestContext(request),
        )


def batch_maint_obl_complete(request):
    """
    Page to display after batch maintenance obligations have been added.
    """
    return render_to_response(
        'tools/maint_obl_batch_complete.html', 
        context_instance = RequestContext(request),
        )



# View restricted to users with is_staff permissions    
@user_passes_test(lambda u: u.is_staff, login_url='/')
def batch_participation_credits(request):
    """
    Provides ability to add multiple participation credits at once. 
    For privileged users (Trackers) only.
    """

    PartCredFormSet = formset_factory(PartCredForm, extra=20)
    if request.method == 'POST':
        formset = PartCredFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset.cleaned_data:
                """
                This shouldn't be necessary - cleaned_data should not pass in empty dictionaries.
                But we're getting them anyway if no data is entered into one of the forms. 
                So we manually skip processing of empty dicts with "if form: "
                """

                if form:
                    credit = Credit()
                    credit.family = form['family']
                    credit.type = 'partpar'
                    credit.date = request.POST['the_date']          
                    credit.amount = form['amount']
                    credit.units = 'hours'
                    credit.note = form['note']                    
                    credit.save()

                    request.user.message_set.create(message="%s participation hour credits added for %s" % (form['amount'], form['family']))

        else:
            request.user.message_set.create(message="Something went wrong. No credits have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")

        # Redirect to a new page to avoid possibility of a browser reload re-adding credits.
        return HttpResponseRedirect("complete")
    else:
        formset = PartCredFormSet()

    return render_to_response(
        'tools/participation_batch.html', 
        {'formset': formset},
        context_instance = RequestContext(request),
        )


def batch_participation_credits_complete(request):
    """
    Page to display after batch participation credits have been added.
    """
    return render_to_response(
        'tools/participation_batch_complete.html', 
        context_instance = RequestContext(request),
        )

# View restricted to superusers
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def batch_board_credit(request,apply=False,period=''):
    """
    We calculate the amount of credit being applied for occupying board positions in the family details view,
    in real time. However, that's just showing the credits, not actually applying them. Once a month this tool 
    is run to add those credits as actual db rows.
    
    Start with list of all families who are due board credits. Use the custom "has_students" manager to 
    make sure we only get families/parents with students that are currently enrolled (so we don't accidentally 
    apply these credits to graduated families).

    Each parent may hold one or more board positions. Get list of all positions 
    occupied by each family. For each in list, determine whether other members
    in the school occupy the same position. If so, split the credit by that 
    number of people.
    
    When "Apply" is clicked, a var called "apply" is sent to the view as True, and we can create
    appropriate Credit objects in the db.
    """
    
    # Get all billing periods for use in the template
    bp_list = BillingPeriod.objects.all().order_by('-start')
    
    # Which billing period should we attach credits to? 
    # Check to see whether period comes in through the URL. 
    # If not, default to current, using our custom manager.
    if period :
        billing_period = BillingPeriod.objects.get(pk=period)
    else :
        try: # Period not specified - try to get one that matches the current date
            billing_period = BillingPeriod.current.get()
        except BillingPeriod.DoesNotExist: # That BillingPeriod was never set up. Set it to None and we'll specify an error in the template.
            billing_period = None
            
    if billing_period:
        apply_date = billing_period.end
        
    # Get list of all parents who occupy board positions
    board_list = BoardPosition.objects.all()
    parent_list = Parent.has_students.filter(board_pos__in=board_list,user__is_active=True)
    board_string = ''
    
    for p in parent_list:
        board_string += "\n\n<p><strong>%s</strong> </p>\n" % p
        board_positions = board_list.filter(parent__exact=p)
        board_string += "<ul>\n"

        for b in board_positions:
            
            # Does anyone else occupy this position? Get number of people who have same position.
            board_credit = 0
            num_other_occupied = len(Parent.has_students.filter(board_pos=b.id))
            board_string += "<li> %s ($%d)\n" % (b, b.credit)
        
            if num_other_occupied > 1 :
                adj_credit = b.credit / num_other_occupied
                board_string += " This position is shared by %d people, including %s. \
                    Adjusted credit: <strong>$%d</strong></li>\n" % (num_other_occupied, p.user.first_name, adj_credit)
                board_credit += adj_credit
                
            else :
                board_string += "This position is not shared. Credit: <strong>$%d</strong></li>\n" % (b.credit)
                board_credit += b.credit
            
            # Report success via built-in messages system
            request.user.message_set.create(message="$%d board credit added for %s" % (board_credit, p.family))
            
            # Create new Credit object in the db
            if apply :
                new_credit = Credit(family=p.family,type='board',date=apply_date,amount=board_credit)
                new_credit.save()
                

    board_string += "</ul>\n"    

    return render_to_response('tools/batch_board_credits.html', 
        {
            'board_string': board_string,       
            'title': "Batch-Add Board Credits",
            'bp_list': bp_list,
            'billing_period': billing_period,
            'apply': apply,                            
        },
        context_instance = RequestContext(request),
    )



# View restricted to superusers
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def summary_charges_credits(request,csv = False,period='',):
    """
    Accountants view - all charges and credits for a given billing period.
    """
    
    # Does billing period come from the URL? If not, show current period.
    if period : 
        billing_period = BillingPeriod.objects.get(pk=period)
    else:
        billing_period = BillingPeriod.current.get()
    
    
    # Need a list of billing periods to send to the template for selector picklists
    bp_list = BillingPeriod.objects.all().order_by('-start')

    # CHARGES
    charges_by_family = Charge.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,).values('family__name').annotate(Sum('charged_amount'))
    total_charges = Charge.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end).aggregate(Sum('charged_amount'))['charged_amount__sum']


    # Get aggregate sums for each of the charge types in models.CHARGE_TYPE_CHOICES. 
    # For each, append to a dictionary where the key has the same name and the value is an aggregate summary of all charges with that name.
    # We'll pass this whole dict to the template.
    
    charge_type_totals = {}
    for c in CHARGE_TYPE_CHOICES :
        # Append key to dict
        charge_type_totals[str(c)] = Charge.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,type=c[0]).aggregate(Sum('charged_amount'))['charged_amount__sum']
    
    credit_type_totals = {}
    for c in CREDIT_TYPE_CHOICES :
        # print c[0]
        # Append key to dict
        credit_type_totals[str(c)] = Credit.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,type=c[0]).aggregate(Sum('charged_amount'))['charged_amount__sum']


    credits_by_family = Credit.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,).values('family__name').annotate(Sum('charged_amount'))
    total_credits = Credit.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end).aggregate(Sum('charged_amount'))['charged_amount__sum']                  

    # Make billing_summary_dict a global so we can use it both in this function and in render_to_csv
    global billing_summary_dict    

    billing_summary_dict = {
        'billing_period': billing_period,
        'period': billing_period,        
        'bp_list':bp_list,
        
        'charges_by_family': charges_by_family,   
        'charge_type_totals': charge_type_totals,
        'total_charges':total_charges, 
        
        'credits_by_family':credits_by_family,
        'credit_type_totals':credit_type_totals,
        'total_credits':total_credits,                                      
    }


    """
    If CSV was passed to this function as True, return output of render_to_csv() 
    for this family. Otherwise return normal HTML.
    """
    if csv:
        return summary_to_csv(request,billing_summary_dict)
    else:
        # Send query result objects to template
        return render_to_response('tools/billing_summary.html', 
            billing_summary_dict,
            context_instance = RequestContext(request),
            )


    
def summary_to_csv(request,billing_summary_dict):
    """
    Output data from view above as CSV.
    """
    response = render_to_response("tools/billing_summary-tables.html", billing_summary_dict,)    
    filename = "billing-summary-data.xls" 
    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
    return response  