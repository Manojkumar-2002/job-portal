from django.db import models
from django.conf import settings
from apps.common.models import AuditTrial


class UserRole(AuditTrial):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    role = models.ForeignKey(
        "access_control.Role",
        on_delete=models.CASCADE,
        related_name="user_roles",
    )

    class Meta:
        db_table = "ac_user_role"
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                condition=models.Q(is_deleted=False),
                name="unique_user_role_active",
            )
        ]

    def __str__(self):
        return f"{self.user.email} → {self.role.name}"
