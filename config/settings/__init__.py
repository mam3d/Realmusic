from decouple import config

if config("PRODUCTION", default=False, cast=bool) == True:
    from .production import *
from .local import *