from .base import *

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = ["*"]

BYPASS_OTPS = ["123456"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env.int("DB_PORT", default=5432),
    }
}
