from .base import *


DEBUG = True
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:1300"]

# settings for django-debug-toolbar
INSTALLED_APPS += ["debug_toolbar", "drf_yasg"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ['172.19.0.1',]
