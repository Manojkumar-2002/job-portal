from django.db import models


class RoleName(models.TextChoices):
    JOBSEEKER = "jobseeker", "Job Seeker"
    EMPLOYER = "employer", "Employer"
    ADMIN = "admin", "Admin"
    MODERATOR = "moderator", "Moderator"


class PermissionCodename(models.TextChoices):
    # jobseeker
    CAN_APPLY_JOB = "can_apply_job", "Can Apply Job"
    CAN_SAVE_JOB = "can_save_job", "Can Save Job"
    CAN_VIEW_JOB = "can_view_job", "Can View Job"
    CAN_MANAGE_JOBSEEKER_PROFILE = "can_manage_jobseeker_profile", "Can Manage Job Seeker Profile"

    # employer
    CAN_POST_JOB = "can_post_job", "Can Post Job"
    CAN_EDIT_JOB = "can_edit_job", "Can Edit Job"
    CAN_DELETE_JOB = "can_delete_job", "Can Delete Job"
    CAN_VIEW_APPLICATIONS = "can_view_applications", "Can View Applications"
    CAN_SHORTLIST_APPLICANT = "can_shortlist_applicant", "Can Shortlist Applicant"
    CAN_REJECT_APPLICANT = "can_reject_applicant", "Can Reject Applicant"
    CAN_MANAGE_EMPLOYER_PROFILE = "can_manage_employer_profile", "Can Manage Employer Profile"

    # moderator
    CAN_APPROVE_JOB = "can_approve_job", "Can Approve Job"
    CAN_REJECT_JOB = "can_reject_job", "Can Reject Job"

    # admin
    CAN_MANAGE_USERS = "can_manage_users", "Can Manage Users"
    CAN_MANAGE_ROLES = "can_manage_roles", "Can Manage Roles"
    CAN_MANAGE_PERMISSIONS = "can_manage_permissions", "Can Manage Permissions"
