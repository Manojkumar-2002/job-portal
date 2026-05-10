from django.db import models

class ProfileType(models.TextChoices):
    JOB_SEEKER = 'job_seeker', 'Job Seeker'
    EMPLOYER = 'employer', 'Employer'