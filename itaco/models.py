from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.localflavor.us.models import *
import datetime, time
from django.db.models import signals
from signals import update_profile
import constants
# from sorl.thumbnail.fields import ThumbnailField
# from sorl.thumbnail import ImageField
from easy_thumbnails.fields import ThumbnailerImageField
from django.template.defaultfilters import slugify

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

def get_student_avatar_path(instance, filename):
    """
    Since students don't have an associated User object, we unfortunately need a
    separate function to define student avatar upload paths.
    """

    parts = str(filename).split(".")
    return 'uploads/student_avatars/' + str(instance.id) + '/' + slugify(parts[0]) + '.' + parts[1]


class ListExtra(models.Model):
    """
    Extra email addresses to be added to mailing lists.
    The listgen tool works on straight queries, but there are always a few outlier addresses
    that need to be added that can't be extracted from queries. This provides a simple
    interface to add those addresses.
    """
    list = models.SlugField(help_text='Should match list name, e.g. &quot;everyone&quot; for everyone@crestmontschool.org.')
    nomail = models.BooleanField(default=False,help_text='User can send to list but does not receive mail from it.')
    addresses = models.TextField(blank=True,help_text='Add addresses here, one per line.')

    def __unicode__(self):
        return u'%s' % (self.list)
        
    class Meta:
        ordering = ['list']        
        
class SchoolYear(models.Model):
    """System tracks school years individually."""
    title = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    grad_class = models.CharField(max_length=6,choices=constants.CLASS_CHOICES, help_text="Students expected to graduate at the end of this period are in what grade?")
    current = models.NullBooleanField(unique=True,null=True,help_text="Select &quot;Yes&quot; for the current year, &quot;Unknown&quot; for all others. Ignore the &quot;No&quot; option. Only one school year may be marked current at a time.")

    class Meta:
        verbose_name_plural = "School Years"
        ordering = ['start']

    def __unicode__(self):
        return u'%s' % (self.title)


class BoardPosition(models.Model):
    title = models.CharField(max_length=100)
    credit = models.IntegerField(help_text="Amount deducted from tuition for holding this position. <b>Only change this when school policy chances.</b> If multiple people hold this position, this credit will automatically be split between them.")
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Board Positions"
        ordering = ['title']

    def __unicode__(self):
        return u'%s' % (self.title)


class CommitteeJob(models.Model):
    title = models.CharField(max_length=64)
    reports_to = models.ForeignKey(BoardPosition)

    class Meta:
        verbose_name_plural = "Committee Jobs"
        ordering = ['title']

    def __unicode__(self):
        # return u'%s' % (self.get_title_display())
        return self.title



class FamilyManager(models.Manager):
    """
    Custom manager for Family model - gives us the ability to easily return a list
    of all families that have one or more students enrolled via
        Family.has_students.all()
    thus excluding families in the system that do not have enrolled students.
    Used in several places, such as the Families roster and the lists of families
    that appear in the picklists in the batch tools.
    """
    def get_query_set(self):
        return super(FamilyManager, self).get_query_set().filter(student__enrolled=True).distinct()


class Family(models.Model):
    famname = models.CharField('Family Name',max_length=128)
    notes = models.TextField(blank=True)
    fa_factor = models.FloatField('Financial Aid Factor',default=1)
    multiple_residence = models.BooleanField(default=False,help_text='Are parents living in separate houses? Check to enable multiple addresses to appear on roster.')

    # Two managers for this model - the first is default (so all families appear in the admin).
    # The second is only invoked when we call Family.has_students.all()  e.g. on Family Roster page.
    objects = models.Manager()
    has_students = FamilyManager()

    # With this line uncommented, the list of families is limited to families with enrolled
    # students everywhere. Unfortunately that includes the admin, where we need access
    # to all familes ever.
    # objects = FamilyManager()

    class Meta:
        verbose_name_plural = "Families"
        ordering = ['famname']

    def get_absolute_url(self):
        return "/family/%s/" % (self.id)

    def __unicode__(self):
        return u'%s' % (self.famname)


class ProfileManager(models.Manager):
    """
    Custom manager for Profile model - gives us the ability to easily return a list
    of all parents that have one or more students enrolled via
        Profile.has_students.all()
    thus excluding parents in the system that do not have enrolled students.
    """
    def get_query_set(self):
        return super(ProfileManager, self).get_query_set().filter(family__student__enrolled=True).order_by('user__last_name').distinct()



class Profile(models.Model):
    """
    A Profile object is a foreignkey to User - you must create a user before creating a Profile.
    """
    user = models.ForeignKey(User,related_name="profileuser")
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
    url = models.URLField('URL',blank=True, verify_exists=True,help_text='Business or personal URL.')
    primary_contact = models.BooleanField('Primary contact for this family?')
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

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

signals.post_save.connect(update_profile, sender=Profile)


class Student(models.Model):
    """
    A student object is NOT a user in the system and is NOT foreign keyed to User.
    Students will never need to log in.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    expected_grad_yr = models.ForeignKey(SchoolYear,blank=True,null=True,help_text="This is an optional field because you may be entering a non-enrolled sibling, who has no grad year. Be sure to select a grad year for enrolled students.")
    family = models.ForeignKey(Family)
    birthdate = models.DateField(null=True,blank=True)
    # We have both enrolled and alumni fields. These might seem redundant, but we have both because not
    # all students who enroll end up graduating. This way we can keep track of them separately.
    # The alumni field is currently used mostly for mailing list membership.
    enrolled = models.BooleanField(default=True,help_text="Enrolled and Alumni are separate b/c not all students who enroll end up graduating. This way we can keep track of them separately.")
    alumni = models.BooleanField(default=False)
    reader = models.CharField(max_length=4, choices=constants.READER_TYPE_CHOICES,blank=True,null=True)
    avatar = ThumbnailerImageField('Student Photo',upload_to=get_student_avatar_path, blank=True,null=True,
        help_text='Please upload an image of your child. Crop the photo in advance so that it\'s mostly square, not rectangular, and no larger than 600px wide.')

    class Meta:
        verbose_name = "Student/Sibling"
        verbose_name_plural = "Students/Siblings"

    def get_absolute_url(self):
        return "/person/%s/" % (self.id)

    def __unicode__(self):
        return u'%s, %s' % (self.last_name, self.first_name)

    # Use UserManager to get the create_user method, etc.
    # objects = UserManager()



class BillingPeriodManager(models.Manager):
    """
    Custom manager for BillingPeriod model - gives us the ability to easily
    retrieve the current billing period with
        BillingPeriod.current.get()
    """

    def get_query_set(self):
        the_date = datetime.date.today
        return super(BillingPeriodManager, self).get_query_set().filter(start__lte=the_date,end__gte=the_date,)



class BillingPeriod(models.Model):
    """Each school year is divided into 12 billing periods."""

    title = models.CharField(max_length=100)
    school_year = models.ForeignKey(SchoolYear)
    start = models.DateField()
    end = models.DateField()

    # Two managers for this model - the first is default (so all billing periods appear in the admin).
    # The second is only invoked when we call BillingPeriod.current.get()  e.g. on Batch Board Credits page.
    objects = models.Manager()
    current = BillingPeriodManager()

    class Meta:
        verbose_name_plural = "Billing Periods"
        ordering = ['start']

    def __unicode__(self):
        return u'%s' % (self.title)



class Credit(models.Model):
    """Credit object tracks accrual of credit due to families"""

    family = models.ForeignKey(Family)
    type = models.CharField(max_length=8, choices=constants.CREDIT_TYPE_CHOICES)
    date = models.DateField(default=datetime.date.today)
    amount = models.FloatField(help_text=constants.CREDIT_UNITS_HELP_TEXT,)
    charged_amount = models.FloatField(help_text='DO NOT ENTER AN AMOUNT HERE. <br />After pressing save, this field will auto-calculate the dollar equivalent of entered hours, based on current hourly rates. <br /> This amount can be adjusted after saving, if necessary.<br /><br />If you need to change the TYPE of charge, delete this one and create a new one.',blank=True,null=True)
    note = models.CharField(blank=True, max_length=255,null=True)

    def __unicode__(self):
        return u'%s' % (self.family)


    def save(self):
        """
        If hours have been entered into the credits we need to turn that
        into an actual dollar amount based on current rates (in settings.py).
        Need to allow for manual overrides of the amount field, so only do the next line if this is a fresh
        insert (record doesn't yet have an ID).
        """
        if not self.id :

            if self.type == 'partpar': # Participating Parent
                self.charged_amount = round(self.amount * settings.PARTPAR_HOURLY, 2)

            if self.type == 'housekp': # Participating Parent
                self.charged_amount = round(self.amount * settings.HOUSEKEEP_HOURLY, 2)

            if self.type == 'aidsub': # Aid Substitute
                self.charged_amount = round(self.amount * settings.AIDSUB_HOURLY, 2)

            if self.type == 'teachsub': # Teacher Substitute
                self.charged_amount = round(self.amount * settings.TEACHSUB_HOURLY, 2)

            if self.type == 'incorbil': # Incorrect billing
                self.charged_amount = round(self.amount, 2)

            if self.type == 'board': # Teacher Substitute
                self.charged_amount = round(self.amount, 2)

        super(Credit, self).save() # Call the "real" save() method.




class Obligation(models.Model):
    """Obligation object tracks accrual of annual family obligations."""

    family = models.ForeignKey(Family)
    type = models.CharField(max_length=8, choices=constants.OBLIGATION_TYPE_CHOICES,help_text=constants.OBL_UNITS_HELP_TEXT)
    amount = models.FloatField(help_text='Number of units above.')
    note = models.CharField(blank=True, max_length=255,null=True)
    date = models.DateField(default=datetime.date.today)
    units = models.CharField(max_length=8, choices=constants.UNIT_CHOICES,blank=True,null=True,help_text='Do NOT select a Unit type when entering a new obligation - this will be auto-filled based on the type of obligation being entered. This field may be edited after saving.')

    def __unicode__(self):
        return u'%s' % (self.family)

    def save(self):
        """
        Custom save() method to auto-enter unit type based on the obligation type selected
        (using CHARGE_TYPE_CHOICES (above) as a map).
        """
        if not self.id :

            if self.type == 'mbsmtg': # Membership Meeting
                self.units = 'units'

            if self.type == 'maint': # Maintenance/Work Party
                self.units = 'hours'

            if self.type == 'fundrais': # Fundraising
                self.units = 'hours'

            if self.type == 'fldtrp': # Field Trip
                self.units = 'units'

            if self.type == 'oblscrp1': # Annual Obligation/Scrip (1 child enrolled)
                self.units = 'dollars'

            if self.type == 'oblscrp2': # Annual Obligation/Scrip (2 child enrolled)
                self.units = 'dollars'

            if self.type == 'housekpg': # Housekeeping
                self.units = 'units'

            if self.type == 'cmt_coop': # Committee/Co-op Job
                self.units = 'units'

        super(Obligation, self).save() # Call the "real" save() method.


class Charge(models.Model):
    """
    Charge object tracks accrual of daycare charges stored as hours. Daycare charges entered as dollars,
    such as Flat Fee daycare, is entered under Charges Other.
    """

    family = models.ForeignKey(Family)
    date = models.DateField(default=datetime.date.today)
    type = models.CharField(max_length=8, choices=constants.CHARGE_TYPE_CHOICES, help_text=constants.CHARGE_AMT_HELP_TEXT)
    amount = models.FloatField()
    units = models.CharField(max_length=8, choices=constants.UNIT_CHOICES, blank=True)
    charged_amount = models.FloatField(help_text='DO NOT ENTER AN AMOUNT HERE. <br />After pressing save, this field will auto-calculate the dollar equivalent of entered hours, based on family financial aid factor and current hourly rates. <br /> This amount can be adjusted after saving, if necessary.',blank=True,null=True)
    note = models.CharField(blank=True, max_length=255,null=True)

    class Meta:
        verbose_name_plural = "Charges"


    def fa_adjusted(self):
        """
        Charge amount adjusted for this family's financial aid factor.
        NOTE: We've moved to inserting FA-adjusted amounts directly into the database rather than calculating
        them at display time. This way we won't get inaccurate data when viewing historical data if family's
        FA factor or the hourly rate for daycare changes. So this method may not be necessary (but leaving in
        just in case it ever is).
        """
        return self.family.fa_factor * self.amount

    def __unicode__(self):
        return u'%s' % (self.family)


    def save(self):
        """
        If hours have been entered into the form for standard daycare charges we need to turn that
        into an actual dollar amount based on financial aid factor and the current hourly rate for regulary daycare.
        Need to allow for manual overrides of the charged_amount field, so only do the next line if this is a fresh
        insert (record doesn't yet have an ID). We also auto-enter unit type based on the charge type selected
        (using CHARGE_TYPE_CHOICES (above) as a map). For amounts in straight dollars, we copy the entered
        amount into charged_amount to make totalling easier.
        """
        if not self.id :
            # We also want to round the totals out to two decimal places when the charge is saved.

            if self.type == 'hrdc': # Hourly regular daycare
                self.units = 'hours'
                self.charged_amount = round(self.amount * settings.DAYCARE_REGULAR_HOURLY * self.family.fa_factor, 2)

            if self.type == 'dihvdc': # Drop-in hourly vacation daycare
                self.units = 'hours'
                self.charged_amount = round(self.amount * settings.DAYCARE_VACATION_DROPIN * self.family.fa_factor, 2)

            if self.type == 'pavdc': # Pre-arranged vacation daycare
                self.units = 'hours'
                self.charged_amount = round(self.amount * settings.DAYCARE_VACATION_PREARRANGE * self.family.fa_factor, 2)

            if self.type == 'edc1': # Event daycare flat fee - 1 child
                self.units = 'dollars'
                self.charged_amount = round(self.amount * settings.DAYCARE_EVENT_1_CHILD, 2)

            if self.type == 'edc2': # Event daycare flat fee - 2 child
                self.units = 'dollars'
                self.charged_amount = round(self.amount * settings.DAYCARE_EVENT_2_CHILD, 2)

            if self.type == 'edc3': # Event daycare flat fee - 3 child
                self.units = 'dollars'
                self.charged_amount = round(self.amount * settings.DAYCARE_EVENT_3_CHILD, 2)

            if self.type == 'dclpu': # Daycare late pickup
                self.charged_amount = round(self.amount * settings.DAYCARE_LATE_PICKUP, 2)

            if self.type == 'mshc': # Missed housecleaning
                self.charged_amount = round(self.amount * settings.MISSED_HOUSECLEANING, 2)

            if self.type == 'mmh': # Missed maintenance
                self.charged_amount = round(self.amount * settings.MISSED_MAINTENANCE_HOURLY, 2)

            if self.type == 'mfrsg': # Missed fundraising
                self.charged_amount = round(self.amount * settings.MISSED_FUNDRAISING, 2)

            if self.type == 'mftr': # Missed fieldtrip
                self.charged_amount = round(self.amount * settings.MISSED_FIELDTRIP, 2)

            if self.type == 'mmtg': # Missed meeting
                self.charged_amount = round(self.amount * settings.MISSED_MEETING, 2)

            if self.type == 'meal': # Meal expense
                self.charged_amount = self.amount


            if self.type == 'adj': # Misc adjustment
                self.units = 'dollars'
                self.charged_amount = round(self.amount, 2)

        super(Charge, self).save() # Call the "real" save() method.



