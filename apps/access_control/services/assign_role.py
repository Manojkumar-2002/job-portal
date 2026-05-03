from ..models import Role, UserRole

def assign_role_to_user(user, role_name):
    # 1. FETCH: It finds the Role object in your 'ac_role' table.
    role = Role.objects.get(name=role_name)
    
    # 2. LINK: It looks for an existing record in 'ac_user_role' 
    # where user=user AND role=role.
    user_role, created = UserRole.objects.get_or_create(
        user=user, 
        role=role,
        defaults={'is_deleted': False}
    )
    
    # 3. REACTIVATE: If the record existed but was 'is_deleted=True',
    # this ensures it becomes 'active' again.
    if not created and user_role.is_deleted:
        user_role.is_deleted = False
        user_role.save()