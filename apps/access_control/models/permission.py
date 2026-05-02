from django.db import models
from apps.common.models import AuditTrial
from apps.access_control.enums import PermissionCodename


class Permission(AuditTrial):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, choices=PermissionCodename.choices)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.codename

    class Meta:
        db_table = "ac_permission"
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        constraints = [
            models.UniqueConstraint(
                fields=["codename"],
                condition=models.Q(is_deleted=False),
                name="unique_permission_codename_active",
            )
        ]
