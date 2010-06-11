"""
If you add models to an app after the inital syncdb, it will not be possible to assign permissions for those new models.
Run this script to fix that.
"""
from django.core.management import setup_environ
try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Couldn't find the settings.py module.")
    sys.exit(1)

setup_environ(settings)

# Add any missing content types
from django.contrib.contenttypes.management import update_all_contenttypes
update_all_contenttypes()

# Add any missing permissions
from django.contrib.auth.management import create_permissions
from django.db.models import get_apps
for app in get_apps():
    create_permissions(app, None, 2)

