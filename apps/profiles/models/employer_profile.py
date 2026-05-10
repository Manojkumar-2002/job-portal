from django.db import models
from django.conf import settings
from apps.common.models import AuditTrial
from apps.profiles.enums import CompanySize


class EmployerProfile(AuditTrial):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employer_profile",
    )
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=20, choices=CompanySize.choices, blank=True)
    address = models.OneToOneField(
        "common.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employer_profile",
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_name} - {self.user.email}"

    class Meta:
        db_table = "profile_employer"
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"
