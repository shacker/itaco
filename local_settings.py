DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'crest_ourdjang'             # Or path to database file if using sqlite3.
DATABASE_USER = 'crest_school'             # Not used with sqlite3.
DATABASE_PASSWORD = 'k00lsk00l'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Media dir referenced from urls.py so media can be served from both runserver and production
STATIC_DOC_ROOT = '/home/crest/sites/crest/ourcrestmont/media'
MEDIA_ROOT = '/home/crest/sites/crest/ourcrestmont/media'


EMAIL_USE_TLS = False
EMAIL_HOST = 'gong.birdhouse.org'
EMAIL_HOST_USER = 'sysmail@our.crestmontschool.org'
DEFAULT_FROM_EMAIL = 'sysmail@our.crestmontschool.org'
EMAIL_HOST_PASSWORD = '+zNNd+p8L2u7'
EMAIL_PORT = 587

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/crest/sites/crest/ourcrestmont/templates',
)

APPEND_SLASH = True

DEBUG = False
TEMPLATE_DEBUG = DEBUG


# Where generated mailing list files will go
LISTGENPATH = "/home/crest/sites/crest/ourcrestmont/scripts/listgen"
