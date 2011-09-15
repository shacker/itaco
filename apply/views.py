from ourcrestmont.itaco.models import Family, Profile, Student, SchoolYear, CommitteeJob, BoardPosition
from apply.models import Application, STATUS_CHOICES
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from ourcrestmont.apply.forms import ApplicationForm
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.template.defaultfilters import slugify
import sys, zipfile, os, os.path, shutil
from django.contrib.auth.models import User


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
           
            # Upon successful submit, we redirect back to the public site - there's nothing here for a non-member to see.
            return HttpResponseRedirect('http://crestmontschool.org/application-received/')            
        # else:
        #     print form.errors
    else:
        form = ApplicationForm()


    return render_to_response('apply/apply.html', 
        {
            'form': form,
        },
        context_instance = RequestContext(request),
    )
    
    

def process_apps(request):
    '''
    View and process outstanding applications. 
    Accepted students get their family, parent, profile, and student objects added automatically.
    Does not yet send accept/reject emails, but could...
    '''
    
    accepted = Application.objects.filter(status=1).order_by('appdate')
    rejected = Application.objects.filter(status=2).order_by('appdate')    
    pending = Application.objects.filter(status=3,fee_paid=False).order_by('appdate')  
    paid_pending = Application.objects.filter(status=3,fee_paid=True).order_by('appdate')        

    return render_to_response('apply/process_apps.html', 
        locals(),
        context_instance = RequestContext(request),
    )    
    
    

def app_detail(request,app_id=None):
    '''
    View all fields of an individual application
    '''
    
    app = get_object_or_404(Application,pk=app_id)
    status_choices = STATUS_CHOICES

    return render_to_response('apply/app_detail.html', 
        locals(),
        context_instance = RequestContext(request),
    )  
    
    
def change_app_status(request):
    '''
    Toggle an application from pending to rejected or accepted
    '''
    
    app = get_object_or_404(Application,pk=request.POST['app_id'])
    
    '''
    If rejected:
        set status to rejected and return to process_apps; show message
    If accepted:
        show warning dialog; create student, family and parent records; show message
    Else:
        return to process_apps, show message
    '''    
    
    if request.POST['app_status'] == '1':
        # Uncomment these after rest of code finished
        # app.status = 1
        # app.save()
        messages.success(request, "Application for %s set to Accepted" % app)
        
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
            # This is probably evidence that I should have designed the the Applications sytem to store
            # User and Profile records to begin with rather than putting everything in a separate record.
            # But too late to turn back now.
            
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
                profile.save()
            except:
                # User creation could fail in the unlikely event that another user sam_jones already exists in the system
                messages.error(request, "Failed creating iTaco user %s. Please contact the webmaster." % user.username)
                
                
            # Second run-through for parent 2
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
            os.makedirs(newdir)
            shutil.copy(oldpath,newdir)
            
            # Now update the student record with new avatar
            filename = os.path.basename(oldpath)
            student.avatar = os.path.join('uploads','student_avatars',str(student.id),str(filename))
            student.save()
            messages.success(request, "Profile image for student copied into student record.")
            
        messages.success(request, "New student record created. Please review the student entry in admin.")
        
    # Reject this app
    elif request.POST['app_status'] == '2':
        app.status = 2
        app.save()
        messages.success(request, "Application for %s set to Rejected" % app)
    
    # Fallback - leave as pending or set back to pending
    elif request.POST['app_status'] == '3':
        messages.success(request, "Application for %s set to Pending" % app)
        
    else:
        # This will probably never happen
        messages.error(request, "Application for %s not changed" % app)        
        
    return HttpResponseRedirect(reverse('process_apps'))
       
       
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
        context_instance = RequestContext(request),
    )  