from django.db import models
from django import forms
from django.forms.formsets import formset_factory
from itaco.models import *
from itaco.constants import *
from itaco.forms import ChargeForm, PartCredForm, OblForm, StudentForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings

# For reading files from listgen output
import sys,os



def listgen(request):
    """
    Listgen script runs externally, via cronjob, and generates text files. This just lets people see who's on the lists.
    """
    # Populate a dictionary mldict with lists for values, like:
    # {kindergarten:[foo,bar],first:[baz,blob]}

    mldict = {}
    nomailmldict = {}
    groupset = ['kindergarten','first','second','third','twothree','fourth','fifth','fourfive','board','teachers','alumni','executivecom','alphageeks','participation','everyone',]
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
    p = Profile.objects.filter(family=fam_id)
    s = Student.objects.filter(family=fam_id,enrolled=True)
    siblings = Student.objects.filter(family=fam_id,enrolled=False)

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
            'siblings': siblings,
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


    """
    Now we can get actual start and stop dates for the current period view.
    All queries below are filtered by greater than / less than these:

    date__gte=period_start,date__lte=period_end
    """


    """
    Get base objects for family, and for parents and students in this family.
    """
    f = get_object_or_404(Family,pk=fam_id)
    p = Profile.objects.filter(family=fam_id)
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
    Removing this for now - Vickie, Amy agree its' currently not needed.
    """
    # num_kids = s.count()
    # if num_kids > 1 :
    #     obl_annual_obligation_due = settings.ANN_OBLIGATION_2_CHILD
    # else:
    #     obl_annual_obligation_due = settings.ANN_OBLIGATION_1_CHILD

    """
    This family may hold one or more board positions. Get list of all positions
    occupied by this family. For each in list, determine whether other members
    in the school occupy the same position. If so, split the credit by that
    number of people.

    Also adjust the number of maintenance obligation hours depending on whether a
    board position is occupied, and whether that board position is shared.
    """
    board_positions = BoardPosition.objects.filter(profile__in=p)
    board_string = ""
    board_credit = 0
    for b in board_positions:
        # Does anyone else occupy this position? Get number of people who have same pos.
        num_other_occupied = len(Profile.objects.filter(board_pos=b.id))
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


    # Need a list of years and a list of billing periods to send to the template for selector picklists
    year_list = SchoolYear.objects.all()
    bp_list = BillingPeriod.objects.all().order_by('-start')

    # Only staff/superuser and the current family can view their own finance details.
    # Since we only need to block from view part of the data in the family-details template,
    # send canview_charges to the template.

    # First obtain the current user's family ID
    try:
        p=Profile.objects.get(user=request.user.id)
        myfam_id=p.family.id
    except:
        myfam_id=None


    if request.user.is_staff:
        canview_charges = 1
    elif myfam_id == f.id : # Uses fam_id from context processor.
        canview_charges = 1
    else:
        canview_charges = 0


    """
    Calculate totals. Blank everything out first.
    """

    total_charge_dollars = ch.aggregate(Sum('charged_amount'))['charged_amount__sum']

    if total_charge_dollars == None: # Can't test for None in template, but can compare to zero; convert
        total_charge_dollars = 0

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
    """
    obl_member_meetings_complete = o.filter(type='mbsmtg').aggregate(Sum('amount'))['amount__sum']

    # This needs to be a sum, not a count - we need total number of hours, not the number of records!
    # Sum() returns a dictionary, so need to access that element of the dictionary.
    # obl_maint_hours_complete = o.filter(type='maint').count()
    obl_maint_hours_complete = o.filter(type='maint').aggregate(Sum('amount'))['amount__sum']

    # Same caveat with fundraising hours
    # obl_fundraising_hours_complete = o.filter(type='fundrais').count()
    obl_fundraising_hours_complete = o.filter(type='fundrais').aggregate(Sum('amount'))['amount__sum']

    obl_field_trips_complete = o.filter(type='fldtrp').aggregate(Sum('amount'))['amount__sum']
    obl_housekeeping_complete = o.filter(type='housekpg').aggregate(Sum('amount'))['amount__sum']
    obl_coop_jobs_complete = o.filter(type='cmt_coop').count()

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
          # 'obl_annual_obligation_due' : obl_annual_obligation_due,

          # Charges
          'charges': ch,
          'daycare_hourly_rate': settings.DAYCARE_REGULAR_HOURLY,
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
          # 'annual_obligation_data' : [obl_annual_obligation_complete + .0001, obl_annual_obligation_due - obl_annual_obligation_complete],

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
def batch_charges(request, *args, **kwargs):
    """
    Provides ability to add multiple charges at once.
    Type of charge (daycare, meals) is provided from a dict coming from URLs.
    For privileged users (Trackers) only.
    """
    # What kind of charges are we adding here? Daycare? Meal?
    type = kwargs.pop('type', None)

    ChargeFormSet = formset_factory(ChargeForm, extra=20)
    if request.method == 'POST':
        formset = ChargeFormSet(request.POST, request.FILES)

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
                    charge.type = type
                    charge.date = request.POST['the_date']
                    charge.amount = form['amount']
                    charge.note = form['note']
                    charge.save()

                    if charge.type == 'hrdc':
                        messages.success(request, "%s daycare hours added for %s" % (form['amount'], form['family']))

                    if charge.type == 'meal':
                        messages.success(request, "%s meal dollars added for %s" % (form['amount'], form['family']))

        else:
            messages.error(request, "Something went wrong. No charges have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")

        if type == 'hrdc':
            return HttpResponseRedirect(reverse('batch_daycare_charges'))
        if type == 'meal':
            return HttpResponseRedirect(reverse('batch_meal_charges'))            
    else:
        formset = ChargeFormSet()

    return render_to_response(
        'tools/charge_batch.html',
        locals(),
        context_instance = RequestContext(request),
        )






#
# # View restricted to users with is_staff permissions
# @user_passes_test(lambda u: u.is_staff, login_url='/')
# def batch_maintenance_obl(request):
#     """
#     Provides ability to add multiple maintenance obligations at once.
#     For privileged users (Trackers) only.
#     """
#
#     MaintOblFormSet = formset_factory(MaintOblForm, extra=20)
#     if request.method == 'POST':
#         formset = MaintOblFormSet(request.POST, request.FILES)
#
#         if formset.is_valid():
#             for form in formset.cleaned_data:
#                 """
#                 This shouldn't be necessary - cleaned_data should not pass in empty dictionaries.
#                 But we're getting them anyway if no data is entered into one of the forms.
#                 So we manually skip processing of empty dicts with "if form: "
#                 """
#
#                 if form:
#                     obl = Obligation()
#                     obl.family = form['family']
#                     obl.type = 'maint'
#                     obl.date = request.POST['the_date']
#                     obl.amount = form['amount']
#                     obl.note = form['note']
#                     # obl.units = 'hours'
#                     obl.save()
#
#                     # request.user.message_set.create(message="%s maintenance hours added for %s" % (form['amount'], form['family']))
#                     messages.success(request, "%s maintenance hours added for %s" % (form['amount'], form['family']))
#
#         else:
#             # request.user.message_set.create(message="Something went wrong. No obligation hours have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")                messages.success(request, "%s maintenance hours added for %s" % (form['amount'], form['family']))
#             messages.error(request, "Something went wrong. No obligation hours have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")
#
#         # Redirect to a new page to avoid possibility of a browser reload re-adding charges.
#         # return HttpResponseRedirect("complete")
#         return HttpResponseRedirect(reverse('batch_maintenance_obl'))
#     else:
#         formset = MaintOblFormSet()
#
#     return render_to_response(
#         'tools/maint_obl_batch.html',
#         {'formset': formset},
#         context_instance = RequestContext(request),
#         )


# View restricted to users with is_staff permissions
@user_passes_test(lambda u: u.is_staff, login_url='/')
def batch_obl(request):
    """
    Provides ability to add multiple obligations of a given type at once.
    For privileged users (Trackers) only.
    """

    OblFormSet = formset_factory(OblForm, extra=20)
    if request.method == 'POST':
        formset = OblFormSet(request.POST, request.FILES)

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
                    # obl.type = 'maint'
                    obl.type = request.POST['type']
                    obl.date = request.POST['the_date']
                    obl.amount = form['amount']
                    obl.note = form['note']
                    obl.save()

                    messages.success(request, "%s maintenance hours added for %s" % (form['amount'], form['family']))

        else:
            messages.error(request, "Something went wrong. No obligation hours have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")

        # Redirect to a new page to avoid possibility of a browser reload re-adding charges.
        return HttpResponseRedirect(reverse('batch_obl'))
    else:
        formset = OblFormSet()

    return render_to_response(
        'tools/batch_obl.html',
        {'formset': formset},
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

                    messages.success(request, "%s participation hour credits added for %s" % (form['amount'], form['family']))
        else:
            messages.error(request, "Something went wrong. No credits have been added.  Most likely one of the forms was missing data (totally empty forms are OK, but half-filled forms are not).  Please click the Back button in your browser, correct any errors, and re-submit.")

        # Redirect to a new page to avoid possibility of a browser reload re-adding credits.
        return HttpResponseRedirect(reverse('batch_participation_credits'))
    else:
        formset = PartCredFormSet()

    return render_to_response(
        'tools/participation_batch.html',
        {'formset': formset},
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
    parent_list = Profile.has_students.filter(board_pos__in=board_list,user__is_active=True)
    board_string = ''

    for p in parent_list:
        board_string += "\n\n<p><strong>%s</strong> </p>\n" % p
        board_positions = board_list.filter(profile__exact=p)
        board_string += "<ul>\n"

        for b in board_positions:

            # Does anyone else occupy this position? Get number of people who have same position.
            board_credit = 0
            num_other_occupied = len(Profile.has_students.filter(board_pos=b.id))
            board_string += "<li> %s ($%d)\n" % (b, b.credit)

            if num_other_occupied > 1 :
                adj_credit = b.credit / num_other_occupied
                board_string += " This position is shared by %d people, including %s. \
                    Adjusted credit: <strong>$%d</strong></li>\n" % (num_other_occupied, p.user.first_name, adj_credit)
                board_credit += adj_credit

            else :
                board_string += "This position is not shared. Credit: <strong>$%d</strong></li>\n" % (b.credit)
                board_credit += b.credit


            # Create new Credit object in the db
            if apply :
                new_credit = Credit(family=p.family,type='board',date=apply_date,amount=board_credit)
                new_credit.save()

                # Report success
                # request.user.message_set.create(message="$%d board credit added for %s" % (board_credit, p.family))
                messages.success(request, "$%d board credit added for %s" % (board_credit, p.family))

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
        try:
            billing_period = BillingPeriod.current.get()
        except:
            billing_period = None

    # print billing_period
    # print billing_period.id
    
    if billing_period: # Don't crash if no current billing period is available
        # Need a list of billing periods to send to the template for selector picklists
        bp_list = BillingPeriod.objects.all().order_by('-start')

        # CHARGES
        # charges_by_family = Charge.objects.values('family').filter(date__gte=billing_period.start,date__lte=billing_period.end,).annotate(Sum('charged_amount'))
        # Can't do this adequately with a single queryset, so we'll return these as a list of dictionaries
        charges_by_family = []
        families = Family.has_students.all()
        for f in families:
            famtot = Charge.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,family=f).aggregate(total=Sum('charged_amount'))
            charges_by_family.append({'fam':f,'famtot':famtot})
            
        total_charges = Charge.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end).aggregate(Sum('charged_amount'))['charged_amount__sum']


        # Get aggregate sums for each of the charge types in models.CHARGE_TYPE_CHOICES.
        # For each, append to a dictionary where the key has the same name and the value is an aggregate summary of all charges with that name.
        # We'll pass this whole dict to the template.

        charge_type_totals = []      
        for c in CHARGE_TYPE_CHOICES :
            # Append dict to list
            charge_type_total = Charge.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,type=c[0]).aggregate(Sum('charged_amount'))
            charge_type_totals.append({'type':c,'total':charge_type_total})
            
        credit_type_totals = []
        for c in CREDIT_TYPE_CHOICES :
            # Append dict to list
            # credit_type_totals[str(c)] = Credit.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,type=c[0]).aggregate(Sum('charged_amount'))['charged_amount__sum']
            credit_type_total = Credit.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,type=c[0]).aggregate(Sum('charged_amount'))['charged_amount__sum']
            credit_type_totals.append({'type':c,'total':credit_type_total})
        # print charge_type_totals

        # credits_by_family = Credit.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,).values('family').annotate(Sum('charged_amount'))
        # Can't do this adequately with a single queryset, so we'll return these as a list of dictionaries
        credits_by_family = []
        families = Family.has_students.all()
        for f in families:
            famtot = Credit.objects.filter(date__gte=billing_period.start,date__lte=billing_period.end,family=f).aggregate(total=Sum('charged_amount'))
            credits_by_family.append({'fam':f,'famtot':famtot})
        
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
            locals(),
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




def edit_student(request,student_id=None):
    """
    Allow families to edit minimal details about a student.
    Make sure only a parent of this student, or a staffer, can edit.
    """
    student = get_object_or_404(Student,pk=student_id)

    # Set default birthdate to today if not given
    if not student.birthdate:
        student.birthdate = datetime.datetime.today

    if request.user.get_profile().family == student.family or request.user.is_staff:

        if request.POST:
            form = StudentForm(request.POST, files=request.FILES, instance=student)

            if form.is_valid():
                student.save()

                messages.success(request, "Student record updated.")
                return HttpResponseRedirect(reverse('family_contact',args=[student.family.id]))

        else:
            form = StudentForm(instance=student)

        return render_to_response('edit_student.html', locals(), context_instance=RequestContext(request))
    else:
        messages.error(request, "Student not changed (insufficient permission)")
        return HttpResponseRedirect(reverse('family_contact',args=[student.family.id]))


    return render_to_response(
        'edit_student.html', locals(),
        context_instance = RequestContext(request),
        )



@user_passes_test(lambda u: u.is_superuser, login_url='/')
def obligation_summary(request,year=None):
    """
    A list of families and their numbers towards field trips, meetings, 
    maintenance, housekeeping and fundraising.
    """
    
    try:
        period = SchoolYear.objects.get(pk=year)
    except:
        period = SchoolYear.objects.get(current=True)

    period_start = period.start
    period_end = period.end

    
    """
    Obligation constants brought in from settings
    """
    obl_maint_hours = settings.ANN_MAINTENANCE_HOURS # This gets adjusted later; 7 hours if family has board position; 4 hours if that position is shared.
    obl_member_meetings = settings.ANN_MEMBER_MEETINGS
    obl_fundraising_hours = settings.ANN_EXTERNAL_FUNDRAISING_HOURS
    obl_housekeeping = settings.ANN_HOUSEKEEPING_SESSIONS
    obl_field_trips = settings.ANN_FIELD_TRIPS
    obl_coop_jobs = settings.ANN_COOP_JOBS
    
    families = Family.objects.all()
    fam_oblist = []
    for f in families:
        
        # Calculate all remaining obligations
        field_trips_completed = Obligation.objects.filter(family=f,date__gte=period_start,date__lte=period_end,type='fldtrp').aggregate(Sum('amount'))['amount__sum']
        meetings_attended = Obligation.objects.filter(family=f,date__gte=period_start,date__lte=period_end,type='mbsmtg').aggregate(Sum('amount'))['amount__sum']
        maint_hours = Obligation.objects.filter(family=f,date__gte=period_start,date__lte=period_end,type='maint').aggregate(Sum('amount'))['amount__sum']
        housekeep_hours = Obligation.objects.filter(family=f,date__gte=period_start,date__lte=period_end,type='housekpg').aggregate(Sum('amount'))['amount__sum']
        fundraising_hours = Obligation.objects.filter(family=f,date__gte=period_start,date__lte=period_end,type='fundrais').aggregate(Sum('amount'))['amount__sum']

        fam_oblist.append({
            'fam':f,
            'field_trips_completed':field_trips_completed,
            'meetings_attended':meetings_attended,
            'maint_hours':maint_hours,
            'housekeep_hours':housekeep_hours,
            'fundraising_hours':fundraising_hours,
            })
        
    

    return render_to_response('obligation_summary.html',
        locals(),
        context_instance = RequestContext(request),
    )
    
    
