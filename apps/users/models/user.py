from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_totp_enabled = models.BooleanField(default=False)
    _totp_secret = models.TextField(blank=True, null=True, db_column="totp_secret")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email

    @property
    def totp_secret(self):
        if not self._totp_secret:
            return None
        f = Fernet(settings.TOTP_ENCRYPTION_KEY.encode())
        return f.decrypt(self._totp_secret.encode()).decode()

    @totp_secret.setter
    def totp_secret(self, raw_secret):
        if raw_secret is None:
            self._totp_secret = None
            return
        f = Fernet(settings.TOTP_ENCRYPTION_KEY.encode())
        self._totp_secret = f.encrypt(raw_secret.encode()).decode()
