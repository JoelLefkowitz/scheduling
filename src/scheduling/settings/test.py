import base64
import os

from .base import *  # noqa: F403
from .local import ALLOWED_HOSTS, DATABASES, DEBUG  # noqa: F401

SECRET_KEY = "_"
FIELD_ENCRYPTION_KEY = base64.urlsafe_b64encode(os.urandom(32)).decode()
