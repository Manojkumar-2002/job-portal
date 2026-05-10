from .jobseeker_views import (
    JobSeekerProfileViewSet,
    JobSeekerEducationViewSet,
    JobSeekerExperienceViewSet,
)
from .employer_views import EmployerProfileViewSet

__all__ = [
    "JobSeekerProfileViewSet",
    "JobSeekerEducationViewSet",
    "JobSeekerExperienceViewSet",
    "EmployerProfileViewSet",
]
