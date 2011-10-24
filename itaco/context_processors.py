from django.contrib.auth.models import Group, User
from itaco.models import Profile, Family


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

