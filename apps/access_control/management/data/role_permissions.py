from .job_seeker_permissions import JOB_SEEKER_PERMISSIONS
from .common_permissions import COMMON_PERMISSIONS
from .employer_permissions import EMPLOYER_PERMISSIONS


# Helper to get just the codenames
common_codes = [p["codename"] for p in COMMON_PERMISSIONS]
employer_codes = [p["codename"] for p in EMPLOYER_PERMISSIONS]
job_seeker_codes = [p["codename"] for p in JOB_SEEKER_PERMISSIONS]

ROLE_PERMISSION_MAPPING = {
    "employer": common_codes + employer_codes,
    "job_seeker": common_codes + job_seeker_codes,
}