from django.db import models
from apps.common.models.audit_trial import AuditTrial


class Skill(AuditTrial):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "common_skill"
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=models.Q(is_deleted=False),
                name="unique_skill_name_active",
            )
        ]
