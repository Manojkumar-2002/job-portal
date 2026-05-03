from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.profiles.views import (
    JobSeekerProfileViewSet,
    JobSeekerEducationViewSet,
    JobSeekerExperienceViewSet,
    EmployerProfileViewSet,
)

router = DefaultRouter()
router.register(r"jobseeker", JobSeekerProfileViewSet, basename="jobseeker-profile")
router.register(r"jobseeker-education", JobSeekerEducationViewSet, basename="jobseeker-education")
router.register(r"jobseeker-experience", JobSeekerExperienceViewSet, basename="jobseeker-experience")
router.register(r"employer", EmployerProfileViewSet, basename="employer-profile")

urlpatterns = [
    path("", include(router.urls)),
]