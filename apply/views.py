from ourcrestmont.itaco.models import Family, Profile, Student, SchoolYear, CommitteeJob, BoardPosition
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse


def apply(request):
    '''
    To avoid creating Users, Families and Students before a family is accepted, and to
    closely mimic the PDF application form, we store everything flat here. Later, if people
    are accepted, we copy fields from an app record into the appropriate models.
    '''

    return render_to_response('apply/apply.html', 
        {
            'foo': 'bar',
        },
        context_instance = RequestContext(request),
    )