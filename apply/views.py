from itaco.models import Family, Profile, Student, SchoolYear, CommitteeJob, BoardPosition
from apply.models import Application, STATUS_CHOICES
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from apply.forms import ApplicationForm, AppEditForm, TeacherAppEditForm
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.defaultfilters import slugify
import sys, zipfile, os, os.path, shutil
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

# Only superusers and teachers and special users can access the app system.
# Some additional controls are put on teachers in the app_detail template.
def can_edit_apps(user):
    return user.has_perm("apply.change_application")


def apply(request):
    '''
    To avoid creating Users, Families and Students before a family is accepted, and to
    closely mimic the PDF application form, we store everything flat here. Later, if people
    are accepted, we copy fields from an app record into the appropriate models.
    '''

    # Submit a new application
    if request.POST:
        form = ApplicationForm(request.POST,files=request.FILES)

        if form.is_valid():
            # Don't commit the save until we've added in the fields we need to set
            app = form.save(commit=False)
            app.appdate = datetime.now()

            # If user is logged in, they are already a Crestmont family and this
            # app should be associated with that family
            if request.user.is_authenticated():
                app.family = request.user.get_profile().family

            app.save()

            # Upon successful submit, redirect to the app fee view for this applicant.
            return HttpResponseRedirect(reverse('app_fee',args=[app.id]))
        else:
            # print form.errors
            pass
    else:
        form = ApplicationForm()


    return render_to_response('apply/apply.html', locals(),
        context_instance = RequestContext(request),
    )


def app_fee(request, app_id):
    '''
    Allow a parent to pay the application fee with PayPal.
    '''

    app = get_object_or_404(Application,pk=app_id)

    return render_to_response('apply/app_fee.html',
        locals(),
        context_instance = RequestContext(request),
    )



def app_fee_thanks(request, app_id):
    '''
    On return from payment gateway, set paid=True
    '''

    app = get_object_or_404(Application,pk=app_id)

    return render_to_response('apply/app_fee_thanks.html',
        locals(),
        context_instance = RequestContext(request),
    )



@user_passes_test(can_edit_apps)
def process_apps(request):
    '''
    View and process outstanding applications.
    Accepted students get their family, parent, profile, and student objects added automatically.
    Does not yet send accept/reject emails, but could...
    '''
    apps = Application.objects.filter(archived=False).order_by('-appdate')

    return render_to_response('apply/process_apps.html',
        locals(),
        context_instance = RequestContext(request),
    )


@user_passes_test(can_edit_apps)
def app_detail(request,app_id=None):
    '''
    View all fields of an individual application
    '''

    app = get_object_or_404(Application,pk=app_id)
    status_choices = STATUS_CHOICES

    # Edit application details
    if request.POST:
        if request.user.is_superuser:
            form = AppEditForm(request.POST,instance=app,files=request.FILES)
        else:
            form = TeacherAppEditForm(request.POST,instance=app,files=request.FILES)

        if form.is_valid():
            app = form.save(commit=False)
            app.staff_notes = form.cleaned_data['staff_notes']
            app.save()
            messages.success(request, "App status and/or notes for %s have been modified" % app)

    else:
        if request.user.is_superuser:
            form = AppEditForm(instance=app)
        else:
            # Show minimal form to teachers
            form = TeacherAppEditForm(instance=app)

    return render_to_response('apply/app_detail.html',
        locals(),
        context_instance = RequestContext(request),
    )


@user_passes_test(can_edit_apps)
def intake(request,app_id):
    """
    Convert an application into a set of records in the iTaco db
    for new student, family and parents. Also sends welcome message.
    """

    app = get_object_or_404(Application,pk=app_id)

    # Get current school year and Membership chairs for use in welcome email
    cur_year = SchoolYear.objects.get(current=True)
    chairs = BoardPosition.objects.get(title='Membership').profile_set.all()

    # Make sure we don't try to perform intake for a student/family/parents twice!
    if app.intake_complete == '1' :
        messages.error(request, "Intake has already occurred for this student. Did not re-intake.")
        return HttpResponseRedirect(reverse('process_apps'))


    if request.POST:

        # Create related student, family, and parent records
        # Applications may have been submitted by existing families or by new families
        # so first get a family object depending on that.

        if app.family:
            family = app.family
        else:
            family = Family()
            family.famname = "%s, %s & %s, %s" % (app.par1_lname,app.par1_fname,app.par2_lname,app.par2_fname,)
            family.save()
            messages.success(request, "New iTaco family created. Review generated family and check name, financial aid, or other details.")

            # Since this is a new family, create User objects and related profile records
            # The duplication of code here is stupid - we repeat the next 20 lines to handle both parents.
            # Is there a better way? Not a huge deal, just not very DRY.

            # First run-through for Parent 1. If you modify any of this, do the same for the Parent 2 block below.
            user = User()
            user.first_name = app.par1_fname
            user.last_name = app.par1_lname
            user.username = "%s_%s" % (slugify(app.par1_fname),slugify(app.par1_lname))
            user.email = app.par1_email
            user.set_password(User.objects.make_random_password(length=8))
            user.active = True
            try:
                user.save()
                messages.success(request, "New iTaco user created and set to active: %s" % user.username)

                # We now have a new User object. Attach a new Profile to them.
                profile = Profile.objects.create(user=user)
                profile.family = family
                profile.address1 = app.par1_address1
                profile.address2 = app.par1_address2
                profile.city = app.par1_city
                profile.state = app.par1_state
                profile.zip = app.par1_zip
                profile.phone_home = app.par1_phone_home
                profile.phone_work = app.par1_phone_work
                profile.phone_mobile = app.par1_phone_mobile
                profile.save()
            except:
                # User creation could fail in the unlikely event that another user sam_jones already exists in the system
                messages.error(request, "Failed creating iTaco user %s. Please contact the webmaster." % user.username)


            # Second run-through for parent 2. Only do this if a 2nd parent exists to avoid creating empty parent objects
            # We'll assume that the existence of a first name for parent2 means we have that parent object
            if app.par2_fname:
                user = User()
                user.first_name = app.par2_fname
                user.last_name = app.par2_lname
                user.username = "%s_%s" % (slugify(app.par2_fname),slugify(app.par2_lname))
                user.email = app.par2_email
                user.set_password(User.objects.make_random_password(length=8))
                user.active = True
                try:
                    user.save()
                    messages.success(request, "New iTaco user created and set to active: %s" % user.username)

                    # We now have a new User object. Attach a new Profile to them.
                    profile = Profile.objects.create(user=user)
                    profile.family = family
                    profile.address1 = app.par2_address1
                    profile.address2 = app.par2_address2
                    profile.city = app.par2_city
                    profile.state = app.par2_state
                    profile.zip = app.par2_zip
                    profile.phone_home = app.par2_phone_home
                    profile.phone_work = app.par2_phone_work
                    profile.phone_mobile = app.par2_phone_mobile
                    profile.save()
                except:
                    # User creation could fail in the unlikely event that another user sam_jones already exists in the system
                    messages.error(request, "Failed creating iTaco user %s. Please contact the webmaster." % user.username)


        # Whether this is a new or old family, need to generate this Student object
        student = Student()
        student.first_name = app.child_first
        student.last_name = app.child_last
        student.family = family
        student.birthdate = app.birthdate
        student.enrolled = True
        student.expected_grad_yr = SchoolYear.objects.get(grad_class=app.grade)
        student.save()

        # Now that we have a student ID, we can create an upload folder for their avatar
        # based on it, and shunt their avatar into it. Need to both move the file on disk
        # AND update the student record field with a corrected upload path

        if app.avatar:
            oldpath = os.path.join(settings.MEDIA_ROOT,str(app.avatar))
            newdir = os.path.join(settings.MEDIA_ROOT,'uploads','student_avatars',str(student.id))
            # Don't crash if source media avatar is missing for some reason
            try:
                os.makedirs(newdir)
                shutil.copy(oldpath,newdir)
            except:
                pass

            # Now update the student record with new avatar
            filename = os.path.basename(oldpath)
            student.avatar = os.path.join('uploads', 'student_avatars', str(student.id), str(filename))
            student.save()
            messages.success(request, "Profile image for student copied into student record.")

        # Send welcome message to parents.
        # We know we'll have an email for the first.
        # Also send to the second if we have it.

        recipients = [app.par1_email, ]
        if app.par2_email:
            recipients.append(app.par2_email)

        email_subject = 'Welcome to iTaco, the Crestmont intranet'
        email_body_txt = request.POST['letter_body']
        msg = EmailMessage(email_subject, email_body_txt, "Crestmont Membership <membership@crestmontschool.org>", recipients)

        if msg.send(fail_silently=False):
            messages.success(request, "Welcome letter sent to %s" % recipients)
            app.sent_offer_letter = True
            app.save()
        else:
            messages.error(request, "Something went wrong. Offer letter NOT sent.")

        # Update the intake_complete field so we don't accidentally intake this app again
        app.intake_complete = 1
        app.save()

        messages.success(request, "New student record created. Please review the student entry in admin.")
        return HttpResponseRedirect(reverse('process_apps'))

    else:
        # Display app intake warning page to admins
        return render_to_response('apply/intake.html',
            locals(),
            context_instance=RequestContext(request),
        )


@user_passes_test(can_edit_apps)
def show_addrs(request):
    '''
    View all email addresses of current applicants
    '''

    apps = Application.objects.all()
    emails = []
    for a in apps:
        if a.par1_email:
            emails.append(a.par1_email)
        if a.par2_email:
            emails.append(a.par2_email)

    return render_to_response('apply/show_addrs.html',
        locals(),
        context_instance=RequestContext(request),
    )


@user_passes_test(can_edit_apps)
def send_offer(request, app_id):
    """When an admin clicks Send Offer on an app, present the offer letter for review, send email on Submit."""

    app = get_object_or_404(Application,pk=app_id)
    cur_year = SchoolYear.objects.get(current=True)
    pay_amount = settings.FIRST_TUITION_PAYMENT
    pay_due_date_1 = settings.PAYMENT_DUE_DATE_1
    pay_due_date_2 = settings.PAYMENT_DUE_DATE_2
    pay_due_date_3 = settings.PAYMENT_DUE_DATE_3
    # Determine who currently holds the position of Membership Chair.
    # Technically this could be a shared position but we'll cheat and just use the first (it's usually just one)
    chair = BoardPosition.objects.get(title='Membership').profile_set.all()[0]

    if request.POST:

        # Send email to parents of applicant.
        # We know we'll have an email for the first.
        # Also send to the second if we have it.
        recipients = [app.par1_email, ]
        if app.par2_email:
            recipients.append(app.par2_email)

        email_subject = 'Your child has been accepted at Crestmont School'
        email_body_txt = request.POST['letter_body']
        msg = EmailMessage(email_subject, email_body_txt, "Crestmont Admissions <admissions@crestmontschool.org>", recipients)
        msg.attach_file(settings.ATTACHMENTS_PATH + '/Crestmont_Contract.pdf')

        if msg.send(fail_silently=False):
            messages.success(request, "Offer letter sent to %s" % recipients)
            app.sent_offer_letter = True
            app.save()
        else:
            messages.error(request, "Something went wrong. Offer letter NOT sent.")

        return HttpResponseRedirect(reverse('process_apps'))

    else:
        # Show letter template for review/editing

        return render_to_response('apply/send_offer_letter.html',
            locals(),
            context_instance=RequestContext(request),
        )


@user_passes_test(can_edit_apps)
def send_eval_letter(request, app_id):
    """Allow kindergarten teacher to send evaluation results emails to parents."""

    # Need test here - does app qualify for an offer letter? Paid, etc.?

    app = get_object_or_404(Application, pk=app_id)
    enrollment_chairs = BoardPosition.objects.get(title='Enrollment').profile_set.all()

    if request.POST:

        # Send email to parents of applicant.
        # We know we'll have an email for the first.
        # Also send to the second if we have it.
        recipients = [app.par1_email, ]
        if app.par2_email:
            recipients.append(app.par2_email)

        email_subject = "Invitation to Crestmont student evaluation meeting"
        email_body_txt = request.POST['letter_body']
        msg = EmailMessage(email_subject, email_body_txt, "Crestmont Admissions <admissions@crestmontschool.org>", recipients)

        # Only send emergency form if this is a non-K application
        if app.grade != 'K':
            msg.attach_file(settings.ATTACHMENTS_PATH + '/Visitor_Emergency_Form.pdf')

        if msg.send(fail_silently=False):
            messages.success(request, "Evaluation results letter sent to %s" % recipients)
            app.sent_eval_letter = True
            app.save()
        else:
            messages.error(request, "Something went wrong. Evaluation letter NOT sent.")

        return HttpResponseRedirect(reverse('process_apps'))

    else:
        # Show letter template for review/editing

        return render_to_response('apply/send_eval_letter.html',
            locals(),
            context_instance=RequestContext(request),
        )
