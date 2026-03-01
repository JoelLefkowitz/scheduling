import os

from .base import *  # noqa: F403

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
FIELD_ENCRYPTION_KEY = os.getenv("DJANGO_FIELD_ENCRYPTION_KEY")

ALLOWED_HOSTS = [os.getenv("DJANGO_HOST_DOMAIN")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": 5432,
    }
}
