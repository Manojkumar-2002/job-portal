from django.db import models
from django.conf import settings
from apps.common.models import AuditTrial


class UserPermission(AuditTrial):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_permissions_custom",
    )
    permission = models.ForeignKey(
        "access_control.Permission",
        on_delete=models.CASCADE,
        related_name="user_permissions",
    )
    is_granted = models.BooleanField(default=True)

    class Meta:
        db_table = "ac_user_permission"
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "permission"],
                condition=models.Q(is_deleted=False),
                name="unique_user_permission_active",
            )
        ]

    def __str__(self):
        status = "granted" if self.is_granted else "revoked"
        return f"{self.user.email} → {self.permission.codename} ({status})"
