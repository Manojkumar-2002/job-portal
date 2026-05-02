from django.db import models
from apps.common.models import AuditTrial
from apps.access_control.enums import RoleName


class Role(AuditTrial):
    name = models.CharField(max_length=50, choices=RoleName.choices)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ac_role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=models.Q(is_deleted=False),
                name="unique_role_name_active",
            )
        ]
