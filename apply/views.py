from ourcrestmont.itaco.models import Family, Profile, Student, SchoolYear, CommitteeJob, BoardPosition
from apply.models import Application
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from ourcrestmont.apply.forms import ApplicationForm
from django import forms
from django.http import HttpResponseRedirect
from datetime import datetime


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
    
    accepted = Application.objects.filter(accepted=1).order_by('appdate')
    rejected = Application.objects.filter(accepted=2).order_by('appdate')    
    pending = Application.objects.filter(accepted=3).order_by('appdate')    

    return render_to_response('apply/process_apps.html', 
        locals(),
        context_instance = RequestContext(request),
    )    
    
    

def app_detail(request,app_id=None):
    '''
    View all fields of an individual application
    '''
    
    app = get_object_or_404(Application,pk=app_id)

    return render_to_response('apply/app_detail.html', 
        locals(),
        context_instance = RequestContext(request),
    )        