from django.db import models
from ourcrestmont.itaco.models import Family, Profile, Student, SchoolYear, CommitteeJob, BoardPosition
from sorl.thumbnail import ImageField
from django.contrib.localflavor.us.models import *
from django.template.defaultfilters import slugify

# Not using the CLASS_CHOICES from iTaco.constants because it includes Alumni
STATUS_CHOICES = (
    ('1','Accepted'),
    ('2','Rejected'),
    ('3','Pending'),    
)

CLASS_CHOICES = (
    ('kind','Kindergarten'),
    ('1st','1st grade'),
    ('2nd','2nd grade'),
    ('3rd','3rd grade'),
    ('4th','4th grade'),
    ('5th','5th grade'),  
)

HEARD_ABOUT_CHOICES = (
    ('friend','Friend'),
    ('event','Information Event'),
    ('prsfly','Preschool Flyer'),
    ('news','Newspaper'),
    ('other','Other (please explain)'),
)

# 
# def get_applicant_avatar_path(instance, filename):
#     """
#     Create a logical filename for applicant's uploaded photo
#     """
# 
#     parts = str(filename).split(".")
#     return 'uploads/applicant_avatars/' + str(instance.id) + '/' + slugify(parts[0]) + '.' + parts[1]


class Application(models.Model):
    """
    Closely mimics the traditional/PDF application.
    """
    family = models.ForeignKey(Family,null=True,blank=True,help_text="Is your family already enrolled at Crestmont? If so, please select your family from the list.")
    child_last = models.CharField("Child's Last Name",blank=False, max_length=100)
    child_first = models.CharField("Child's First Name",blank=False, max_length=100)    
    appdate = models.DateField('Application date',blank=True,)
    grade = models.CharField('Applying for grade',max_length=6,choices=CLASS_CHOICES,blank=False,)
    rq_start_date = models.DateField('Requested start date',blank=False,)
    sex = models.CharField(blank=False, max_length=2,choices=(('m','Male'),('f','Female')))
    birthdate = models.DateField('Birth date',blank=False,)
    langs = models.CharField('Languages spoken',blank=True, max_length=255)
    
    # Parent/guardians. Could have subclassed Profile object for this, but this 
    # is a more limited set of fields, and that prob. wouldn't have saved any work.
    
    par1_lname = models.CharField('Parent 1 Last Name',blank=False, max_length=100)
    par1_fname = models.CharField('Parent 1 First Name',blank=False, max_length=100)    
    par1_email = models.EmailField('Email',blank=False)
    par1_address1 = models.CharField('Address 1',max_length=100)
    par1_address2 = models.CharField('Address 2',max_length=100,blank=True)
    par1_city = models.CharField('City',max_length=30)
    par1_state = USStateField('State',default='CA')
    par1_zip = models.CharField('Zip',max_length=10)
    par1_phone_home = PhoneNumberField('Home/mobile phone',blank=True)
    par1_phone_work = PhoneNumberField('Work phone',blank=True)
    
    par2_lname = models.CharField('Parent 2 Last Name',blank=True, max_length=100)
    par2_fname = models.CharField('Parent 2 First Name',blank=True, max_length=100)    
    par2_email = models.EmailField('Email',blank=True)
    par2_address1 = models.CharField('Address 1',max_length=100,blank=True)
    par2_address2 = models.CharField('Address 2',max_length=100,blank=True)
    par2_city = models.CharField('City',max_length=30,blank=True)
    par2_state = USStateField('State',default='CA',blank=True)
    par2_zip = models.CharField('Zip',max_length=10,blank=True)
    par2_phone_home = PhoneNumberField('Home/mobile phone',blank=True)
    par2_phone_work = PhoneNumberField('Work phone',blank=True)    
    
    living = models.TextField('Living arrangement',help_text="What is your child's living arrangement? Who is the legal guardian?")
    cur_school = models.CharField('Current school',blank=True, max_length=120)
    cur_grade = models.CharField('Current grade',max_length=6,choices=CLASS_CHOICES,blank=True,)
    cur_school_addr = models.CharField('Current school address',blank=True, max_length=160)
    cur_school_phone = models.CharField('Current school phone',blank=True, max_length=20)    
    cur_teacher = models.CharField('Current teacher',blank=True, max_length=20)        

    prev_school1 = models.CharField('Previous school',blank=True, max_length=40)        
    prev_school1_phone = models.CharField('Phone',blank=True, max_length=20)            
    prev_school1_dates = models.CharField('Dates',blank=True, max_length=40)  
    
    prev_school2 = models.CharField('Previous school',blank=True, max_length=40)        
    prev_school2_phone = models.CharField('Phone',blank=True, max_length=20)            
    prev_school2_dates = models.CharField('Dates',blank=True, max_length=40)
    
    prev_school3 = models.CharField('Previous school',blank=True, max_length=40)        
    prev_school3_phone = models.CharField('Phone',blank=True, max_length=20)            
    prev_school3_dates = models.CharField('Dates',blank=True, max_length=40)                  

    describe_play = models.TextField('Interaction',blank=False,help_text="Please describe your child's play and interaction with others.")
    describe_special = models.TextField('Qualities',blank=False,help_text='Describe what is special about your child:')
    describe_needs = models.TextField('Needs',blank=False,help_text="Describe any special needs your child may have learning, emotional, social, physical:")
    describe_circumstances = models.TextField('Circumstances',blank=False,help_text="Are there any circumstances that might affect your child's learning (Divorce or separation, death in the family, illness, sibling birth, etc.)")
    describe_seeking = models.TextField('Seeking',blank=False,help_text='What kind of education are you seeking for your child?:')
    describe_contribution = models.TextField('Contribution',blank=False,help_text='How do you see yourself participating in a parent co-op?')

    heard_about = models.CharField('Referred by',max_length=6,choices=HEARD_ABOUT_CHOICES,blank=False,help_text='How did you hear about Crestmont?')
    
    avatar = ImageField('Child photo',upload_to='uploads/applicant_avatars', blank=True,null=True,
        help_text='Please upload an image of your child. Please make sure the photo is mostly square, not rectangular.')    
    
    notes = models.TextField('Notes',blank=True,help_text="Anything else you'd like us to know?")
    status = models.CharField('Application status',max_length=2,choices=STATUS_CHOICES,default=3,blank=False,)
    
    def __unicode__(self):
        return u'%s %s' % (self.child_last, self.child_first)
        
