# Django settings for ourcrestmont project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Scot Hacker', 'shacker@birdhouse.org'),
)

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e4tal2awmr310ezp09df!=yy(klri$uh$&xg$#5m7jjxr(waz5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    # 'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.app_directories.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',    
    'ourcrestmont.middleware.login_req.LoginRequiredMiddleware',
    
)

LOGIN_URL = '/accounts/login/'

LOGIN_EXEMPT_URLS = (
    r'^accounts/password/reset/', # Users with forgotten passwords must be able to access password reset form.
    r'^site_media/', # Without this, user gets no CSS or images until logged in.
)


ROOT_URLCONF = 'ourcrestmont.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.databrowse',
    'django.contrib.messages',    
    'ourcrestmont.itaco',
    'ourcrestmont.roster',
    'ourcrestmont.apply',
    # 'filebrowser',
    'sorl.thumbnail',
    'profiles',
    'django_extensions',

)


TEMPLATE_CONTEXT_PROCESSORS = (
    "ourcrestmont.itaco.context_processors.family_id", # Custom processor to get current user's family ID into every page.
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",

)


# Our custom Django profiles are held in the Profile model, which inherits from User
AUTH_PROFILE_MODULE = 'itaco.Profile'


# Annual obligations (in units per family) as specified in Crestmont Contract
ANN_MEMBER_MEETINGS = 9
ANN_MAINTENANCE_HOURS = 10
ANN_MAINTENANCE_HOURS_BOARD = 4 # Lower maint hours obligation if board position is occupied
ANN_MAINTENANCE_HOURS_BOARD_SHARED = 7 # Lower maint hours obligation if board position is occupied and that position is also shared
ANN_EXTERNAL_FUNDRAISING_HOURS = 2
ANN_OBLIGATION_1_CHILD = 300
ANN_OBLIGATION_2_CHILD = 390
ANN_HOUSEKEEPING_SESSIONS = 3
ANN_FIELD_TRIPS = 3
ANN_COOP_JOBS = 1

# Charge conversions (dollars per hour)

DAYCARE_REGULAR_HOURLY = 6
DAYCARE_VACATION_DROPIN = 7.3
DAYCARE_VACATION_PREARRANGE = 6.8
DAYCARE_EVENT_1_CHILD = 6
DAYCARE_EVENT_2_CHILD = 10
DAYCARE_EVENT_3_CHILD = 12
DAYCARE_LATE_PICKUP = 1
MISSED_MAINTENANCE_HOURLY = 25 
MISSED_HOUSECLEANING = 130
MISSED_FUNDRAISING = 25
MISSED_FIELDTRIP = 50
MISSED_MEETING = 25

# Credit conversions (dollars per hour)
PARTPAR_HOURLY = 8
HOUSEKEEP_HOURLY = 60
AIDSUB_HOURLY = 12
TEACHSUB_HOURLY = 14



# Directory where generated mailing list files will go - override in local_settings
LISTGENPATH = ""


#####################################################################
# Settings go above this line.
# This allows local settings to override.
#####################################################################
try:
    from ourcrestmont.local_settings import *
except ImportError, exp:
    pass
