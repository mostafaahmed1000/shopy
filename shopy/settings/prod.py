from shopy.settings.local import DATABASES
from .base import *

DEBUG = False

ADMINS = [("admin", "admin@test.com")]

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

