# Django settings for ourcrestmont project.

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Scot Hacker', 'shacker@birdhouse.org'),
)

MANAGERS = ADMINS
PROJECT_DIR = os.path.realpath(os.path.dirname(__file__))

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


# Full and relative paths to media and static

MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")
MEDIA_URL = "/media/"

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)
STATIC_URL = "/static/"

# Path to location of files that will be attached to emails. Override in local.
ATTACHMENTS_PATH = ''


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
    'middleware.login_req.LoginRequiredMiddleware',
    
)

LOGIN_URL = '/accounts/login/'

LOGIN_EXEMPT_URLS = (
    r'^accounts/password/reset/', # Users with forgotten passwords must be able to access password reset form.
    r'^site_media/', # Without this, user gets no CSS or images until logged in.
    r'^apply/.*$', # Non-members are allowed to apply to the school
)

# Override in local_settings so we don't have to hard-code the project name here.
ROOT_URLCONF = ''


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.databrowse',
    'django.contrib.messages', 
    'django.contrib.staticfiles',   
    'itaco',
    'roster',
    'apply',
    'easy_thumbnails',
    'profiles',
    'django_extensions',

)


TEMPLATE_CONTEXT_PROCESSORS = (
    "itaco.context_processors.family_id", # Custom processor to get current user's family ID into every page.
    "itaco.context_processors.cur_year", # Custom processor to get current user's family ID into every page.    
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.static",
    'django.contrib.messages.context_processors.messages',
)




# THUMBNAIL_PREFIX = '/cache/'
# THUMBNAIL_CACHE_TIMEOUT = 3600 * 24 * 365

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
# DAYCARE_VACATION_DROPIN = 7.3
DAYCARE_VACATION = 6.0
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

# Constants needed for sending of application offer letters
FIRST_TUITION_PAYMENT = 333
PAYMENT_DUE_DATE_1 = 'March 18, 2012'
PAYMENT_DUE_DATE_2 = 'May 1, 2012'
PAYMENT_DUE_DATE_3 = 'June 1, 2012'

# Directory where generated mailing list files will go - override in local_settings
LISTGENPATH = ""


# TinyMCE admin config
# For admin use we call the config in media/js/tinymce_kdmc_setup.js.

TINYMCE_ADMIN_CONFIG={
  'theme': "advanced", 
  'relative_urls': False, 
  'remove_linebreaks': False, 
  'convert_urls': True, 
  # 'width':'800px',
  # 'height':'300px',
  'plugins': "advimage,advlink,fullscreen,paste,media,searchreplace,template,table,spellchecker",
  'paste_auto_cleanup_on_paste' : True,
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "bottom",
    'theme_advanced_buttons1': "|formatselect,styleselect,|,bold,italic,underline,|,bullist,numlist,blockquote,|,undo,redo,|,link,unlink,|,image,|search,|,pasteword,media,charmap,|,code,|,table,cleanup",
    'theme_advanced_buttons2': "",
    'theme_advanced_buttons3': "",
    'theme_advanced_buttons1_add_before':'spellchecker',    
    'theme_advanced_path': 'false',
    'theme_advanced_blockformats': "p,h2,h3,h4,pre",
    'theme_advanced_styles': "[all] clearfix=clearfix;[p] small=small;[img] Image left-aligned=img_left;[img] Image left-aligned (nospace)=img_left_nospacetop;[img] Image right-aligned=img_right;[img] Image right-aligned (nospace)=img_right_nospacetop;[img] Image Block=img_block;[img] Image Block (nospace)=img_block_nospacetop;[div] column span-2=column span-2;[div] column span-4=column span-4;[div] column span-8=column span-8",
    'theme_advanced_resizing ': 'true',
    'theme_advanced_resize_horizontal ': 'false',
    'theme_advanced_resizing_use_cookie ': 'true',
    'theme_advanced_styles': "Image left-aligned=alignleft;Image right-aligned=alignright;Image w/border=image-border",
    'advlink_styles': "intern=internal;extern=external",
  'content_css' : "/static/css/tiny_editor.css",
  'file_browser_callback': "CustomFileBrowser", 
}


#####################################################################
# Settings go above this line.
# This allows local settings to override.
#####################################################################
try:
    from local_settings import *
except ImportError, exp:
    pass
