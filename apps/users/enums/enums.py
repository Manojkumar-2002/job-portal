from django.db import models


class UserRole(models.TextChoices):
    JOBSEEKER = "jobseeker", "Job Seeker"
    EMPLOYER = "employer", "Employer"
    ADMIN = "admin", "Admin"
