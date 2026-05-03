from rest_framework import permissions
from apps.access_control.models import UserRole
from ..constants import ProfileType

# 1. Base class that queries the database
class BaseRolePermission(permissions.BasePermission):
    role_name = None  # To be overridden by subclasses ('employer' or 'job_seeker')

    def has_permission(self, request, view):
        # Always check authentication first
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Security: Query the database for the truth
        return UserRole.objects.filter(
            user=request.user,
            role__name=self.role_name,
            is_deleted=False
        ).exists()

# 2. Specific, readable classes
class IsEmployer(BaseRolePermission):
    role_name = ProfileType.EMPLOYER

class IsJobSeeker(BaseRolePermission):
    role_name = ProfileType.JOB_SEEKER

class IsOwner(permissions.BasePermission):
    """
    Checks object-level ownership.
    """
    def has_object_permission(self, request, view, obj):
        # If the object is a Profile (has 'user' field)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # If the object is Education/Experience (has 'jobseeker_profile' field)
        if hasattr(obj, 'jobseeker_profile'):
            return obj.jobseeker_profile.user == request.user
            
        return False