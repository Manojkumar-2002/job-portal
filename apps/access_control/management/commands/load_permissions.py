from django.core.management.base import BaseCommand
from apps.access_control.models import Permission, Role, RolePermission
from ..data import COMMON_PERMISSIONS, EMPLOYER_PERMISSIONS, JOB_SEEKER_PERMISSIONS, ROLE_PERMISSION_MAPPING

class Command(BaseCommand):
    help = "Syncs permissions, roles, and links."

    def handle(self, *args, **options):
        # 1. Sync all permissions
        all_perms = COMMON_PERMISSIONS + EMPLOYER_PERMISSIONS + JOB_SEEKER_PERMISSIONS
        for p in all_perms:
            Permission.objects.update_or_create(
                codename=p["codename"],
                defaults={"name": p["name"], "description": p["description"], "is_deleted": False}
            )
        self.stdout.write(self.style.SUCCESS("All permissions synced."))

        # 2. Sync Roles
        for role_name in ROLE_PERMISSION_MAPPING.keys():
            Role.objects.update_or_create(
                name=role_name,
                defaults={"description": f"{role_name.capitalize()} role", "is_deleted": False}
            )
        
        # 3. Link Roles to Permissions
        for role_name, permission_codenames in ROLE_PERMISSION_MAPPING.items():
            role = Role.objects.get(name=role_name)
            
            for codename in permission_codenames:
                permission = Permission.objects.get(codename=codename)
                RolePermission.objects.update_or_create(
                    role=role,
                    permission=permission,
                    defaults={"is_deleted": False}
                )
                
        self.stdout.write(self.style.SUCCESS("Roles and RolePermissions linked successfully."))