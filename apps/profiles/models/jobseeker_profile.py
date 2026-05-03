from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from apps.common.models import AuditTrial
from apps.profiles.enums import GenderChoice


class JobSeekerProfile(AuditTrial):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobseeker_profile",
    )
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GenderChoice.choices, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.OneToOneField(
        "common.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobseeker_profile",
    )
    experience_years = models.PositiveIntegerField(default=0)
    skills = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
        help_text="List of skill names from predefined Skill master",
    )
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - JobSeeker"

    class Meta:
        db_table = "profile_jobseeker"
        verbose_name = "Job Seeker Profile"
        verbose_name_plural = "Job Seeker Profiles"
