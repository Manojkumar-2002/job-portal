from django.db import models
from apps.common.models import AuditTrial


class JobSeekerEducation(AuditTrial):
    jobseeker_profile = models.ForeignKey(
        "profiles.JobSeekerProfile",
        on_delete=models.CASCADE,
        related_name="educations",
    )
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

    class Meta:
        db_table = "profile_jobseeker_education"
        verbose_name = "Job Seeker Education"
        verbose_name_plural = "Job Seeker Educations"
        ordering = ["-start_date"]
