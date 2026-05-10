from rest_framework.permissions import IsAuthenticated
from apps.common.views import BaseProfileViewSet
from apps.profiles.models import JobSeekerProfile, JobSeekerEducation, JobSeekerExperience
from apps.profiles.serializers import (
    JobSeekerProfileSerializer, 
    JobSeekerProfileDetailSerializer, 
    JobSeekerEducationSerializer, 
    JobSeekerExperienceSerializer
)
from apps.common.permissions import IsOwner, IsJobSeeker
from django.db import transaction
from apps.access_control.services.assign_role import assign_role_to_user


        
class JobSeekerProfileViewSet(BaseProfileViewSet):
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsJobSeeker]

    def get_serializer_class(self):
        # Use Detail serializer for fetching full profile, otherwise default
        if self.action == "retrieve":
            return JobSeekerProfileDetailSerializer
        return JobSeekerProfileSerializer

    def get_queryset(self):
        # Optimizing: select_related for 1-to-1, prefetch for reverse foreign keys
        return JobSeekerProfile.objects.filter(
            user=self.request.user
        ).select_related('user', 'address').prefetch_related('educations', 'experiences')

    def perform_create(self, serializer):
        with transaction.atomic():
            # 1. Save the profile
            serializer.save(user=self.request.user)
            
            # 2. Assign the role (This only happens when a new profile is created)
            assign_role_to_user(self.request.user, 'job_seeker')

class JobSeekerEducationViewSet(BaseProfileViewSet):
    queryset = JobSeekerEducation.objects.all()
    serializer_class = JobSeekerEducationSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsJobSeeker]

    def get_queryset(self):
        # Optimizing: only join the parent profile table
        return JobSeekerEducation.objects.filter(
            jobseeker_profile__user=self.request.user
        ).select_related('jobseeker_profile')


class JobSeekerExperienceViewSet(BaseProfileViewSet):
    queryset = JobSeekerExperience.objects.all()
    serializer_class = JobSeekerExperienceSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsJobSeeker]

    def get_queryset(self):
        # Optimizing: only join the parent profile table
        return JobSeekerExperience.objects.filter(
            jobseeker_profile__user=self.request.user
        ).select_related('jobseeker_profile')