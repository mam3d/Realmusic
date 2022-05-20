from .base import *


DEBUG = True

# settings for django-debug-toolbar
INSTALLED_APPS += ["debug_toolbar", "drf_yasg"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ['172.18.0.1',]