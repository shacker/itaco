from django.contrib.auth.models import Group, User
from itaco.models import Profile, Family, SchoolYear


def family_id(request):
    """
    Additional info about the user's request, passed to every template.
    """
    # We always need to know which family the current user belongs to.
    # If user is not logged in or user does not have a family, send none
    try:
        p=Profile.objects.get(user=request.user.id)
        myfam_id=p.family.id
    except:
        myfam_id=None

    return {
        'myfam_id': myfam_id,
    }

def cur_year(request):
    '''
    Discover current school year
    '''
    try:
        cur_year = SchoolYear.objects.get(current=True)
    except:
        '''
        Not ideal to fall back on a particular year like this,
        but many parts of the site rely on there being a cur_year
        available everywhere, and by picking one we can at least
        still access the admin. This will only ever kick in
        if someone sets NO current year in the admin, which is
        briefly required during the transition between years.
        '''
        cur_year = SchoolYear.objects.get(title='2011 - 2012')

    return {
        'cur_year':  cur_year,
    }

