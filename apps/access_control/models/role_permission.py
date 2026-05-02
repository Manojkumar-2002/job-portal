from django.db import models
from apps.common.models import AuditTrial


class RolePermission(AuditTrial):
    role = models.ForeignKey(
        "access_control.Role",
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )
    permission = models.ForeignKey(
        "access_control.Permission",
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )

    class Meta:
        db_table = "ac_role_permission"
        verbose_name = "Role Permission"
        verbose_name_plural = "Role Permissions"
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"],
                condition=models.Q(is_deleted=False),
                name="unique_role_permission_active",
            )
        ]

    def __str__(self):
        return f"{self.role.name} → {self.permission.codename}"
