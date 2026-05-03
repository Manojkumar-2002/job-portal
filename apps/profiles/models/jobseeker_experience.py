from django.db import models
from apps.common.models import AuditTrial


class JobSeekerExperience(AuditTrial):
    jobseeker_profile = models.ForeignKey(
        "profiles.JobSeekerProfile",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    class Meta:
        db_table = "profile_jobseeker_experience"
        verbose_name = "Job Seeker Experience"
        verbose_name_plural = "Job Seeker Experiences"
        ordering = ["-start_date"]
