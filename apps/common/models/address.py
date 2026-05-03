from django.db import models
from apps.common.models.audit_trial import AuditTrial
from ..constants import ProfileType

class Address(AuditTrial):
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    profile_type = models.CharField(
        max_length=20,
        choices=ProfileType.choices,
        default=ProfileType.JOB_SEEKER
    )

    def __str__(self):
        parts = filter(None, [self.street, self.city, self.state, self.country, self.postal_code])
        return ", ".join(parts)

    class Meta:
        db_table = "common_address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
