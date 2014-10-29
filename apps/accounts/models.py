from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.db.models import signals
from signals import update_profile

# from sorl.thumbnail.fields import ThumbnailField
# from sorl.thumbnail import ImageField
from easy_thumbnails.fields import ThumbnailerImageField
from localflavor.us.models import *
from itaco.models import Family, BoardPosition, CommitteeJob, ListExtra


def get_avatar_path(instance, filename):
    """
    Clean the filename and determine the foldername to upload avatars to.
    Must be defined before the Profile class.
    """

    # To keep filenames clean, take the first part of the filename and run it
    # through django's slugify function (if you run the whole thing through,
    # you lose the "." separator in the filename.)
    parts = str(filename).split(".")
    return 'uploads/avatars/' + instance.user.username + '/' + slugify(parts[0]) + '.' + parts[1]


class ProfileManager(models.Manager):
    """
    Custom manager for Profile model - gives us the ability to easily return a list
    of all parents that have one or more students enrolled via
        Profile.has_students.all()
    thus excluding parents in the system that do not have enrolled students.
    """
    def get_queryset(self):
        return super(ProfileManager, self).get_query_set().filter(family__student__enrolled=True).order_by('user__last_name').distinct()



class Profile(UserenaBaseProfile):
    """
    A Profile object is a foreignkey to User - you must create a user before creating a Profile.
    """
    user = models.OneToOneField(User)
    family = models.ForeignKey(Family,blank=True,null=True)
    avatar = ThumbnailerImageField('Personal Photo / Headshot',
        upload_to=get_avatar_path, blank=True,null=True,
        resize_source=dict(size=(800, 600), crop='smart'),
        help_text='Upload an image of yourself! Please make sure your photo is mostly square, not rectangular.')

    title = models.CharField(blank=True, max_length=100,help_text='e.g. Third Grade Teacher. Right now this is only used for teachers, but could be used for anyone in the future.')
    about = models.TextField(blank=True,help_text="Tell us a bit about yourself - interests, work, favorite bands... <br />This field will be displayed on your Profile page.")
    tags = models.CharField(blank=True, max_length=255,help_text="Comma-separated keywords. Not displayed on site, but helps your profile get found in site Search.")
    email_2 = models.EmailField('Secondary email',blank=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=30)
    state = USStateField(default='CA')
    zip = models.CharField(max_length=10)
    phone_home = PhoneNumberField(blank=True)
    phone_work = PhoneNumberField(blank=True)
    phone_mobile = PhoneNumberField(blank=True)
    fax = PhoneNumberField(blank=True)
    participating_parent = models.BooleanField(default=False,help_text="Parent participates in classes. If checked, parent will end up on the participating@ mailing list.")
    no_lists = models.BooleanField(default=False,help_text="When checked, this parent will NOT be subscribed to the mailing lists they normally would be.")
    twitter = models.CharField(blank=True, max_length=100, help_text='Your username on Twitter, e.g. &quot;joebob&quot;.')
    facebook = models.CharField(blank=True, max_length=100, help_text='Your username on FaceBook, e.g. &quot;janedoe&quot;. <br />Get a FaceBook username <a href=http://www.facebook.com/username/>here</a>.')
    url_title = models.CharField('URL Title',blank=True, max_length=120, help_text='Title of your business or personal URL.')
    url = models.URLField('URL',blank=True, help_text='Business or personal URL.')
    primary_contact = models.BooleanField('Primary contact for this family?', default=False)
    board_pos = models.ManyToManyField(BoardPosition,help_text="Select the BOARD position(s) this person currently holds.",verbose_name='Board Position',blank=True)
    comm_job = models.ManyToManyField(CommitteeJob,help_text="Select the COMMITTEE JOB(s) (family job) this person currently holds.",verbose_name='Committee Job',blank=True)
    has_timesheet = models.BooleanField(default=False,help_text="Enable for staff/faculty who use hourly timesheets (Treasurer will upload via FTP; will become available from members Profile page.)")

    # To find all of this person's additional mailing lists, use profile.list_extras.all()
    list_extras = models.ManyToManyField(ListExtra, blank=True, help_text="Everyone is AUTOMATICALLY added to the lists to which they logically belong. Add ADDITIONAL lists here.")

    # Two managers for this model - the first is default (so all parents appear in the admin).
    # The second is only invoked when we call Profile.has_students.all()  e.g. on Parents Roster page.
    objects = models.Manager()
    has_students = ProfileManager()


    def __unicode__(self):
        return u'%s, %s' % (self.user.last_name, self.user.first_name)

    # Looks redundant with above, but needed for the list_display on this model
    def profile_name(self):
        return u'%s, %s' % (self.user.last_name, self.user.first_name)

    def friendly_name(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

signals.post_save.connect(update_profile, sender=Profile)