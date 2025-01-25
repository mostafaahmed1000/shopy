from shopy.settings.local import DATABASES
from .base import *

DEBUG = False

ADMINS = [("admin", "admin@test.com")]

ALLOWED_HOSTS = ["*"]

DATABASES = {"default": {}}
