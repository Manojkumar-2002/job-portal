from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.profiles.models import (
    JobSeekerProfile,
    JobSeekerEducation,
    JobSeekerExperience,
)
from apps.profiles.serializers import (
    JobSeekerProfileSerializer,
    JobSeekerProfileDetailSerializer,
    JobSeekerEducationSerializer,
    JobSeekerExperienceSerializer,
)


class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for JobSeeker Profile management"""

    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return JobSeekerProfileDetailSerializer
        return JobSeekerProfileSerializer

    def get_queryset(self):
        # Users can only see their own profile or admins can see all
        if self.request.user.is_staff:
            return JobSeekerProfile.objects.all()
        return JobSeekerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current authenticated user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure user can only update their own profile
        if serializer.instance.user != self.request.user:
            raise serializers.ValidationError("You can only update your own profile")
        serializer.save()



class JobSeekerEducationViewSet(viewsets.ModelViewSet):
    """ViewSet for JobSeeker Education management"""

    queryset = JobSeekerEducation.objects.all()
    serializer_class = JobSeekerEducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see education records for their own profile
        if self.request.user.is_staff:
            return JobSeekerEducation.objects.all()
        return JobSeekerEducation.objects.filter(jobseeker_profile__user=self.request.user)

    def perform_create(self, serializer):
        # Auto-create profile if it doesn't exist yet
        profile, created = JobSeekerProfile.objects.get_or_create(user=self.request.user)
        serializer.save(jobseeker_profile=profile)

    def perform_update(self, serializer):
        # Ensure user can only update their own education
        if serializer.instance.jobseeker_profile.user != self.request.user:
            raise serializers.ValidationError("You can only update your own education records")
        serializer.save()


class JobSeekerExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet for JobSeeker Experience management"""

    queryset = JobSeekerExperience.objects.all()
    serializer_class = JobSeekerExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see experience records for their own profile
        if self.request.user.is_staff:
            return JobSeekerExperience.objects.all()
        return JobSeekerExperience.objects.filter(jobseeker_profile__user=self.request.user)

    def perform_create(self, serializer):
        # Auto-create profile if it doesn't exist yet
        profile, created = JobSeekerProfile.objects.get_or_create(user=self.request.user)
        serializer.save(jobseeker_profile=profile)

    def perform_update(self, serializer):
        # Ensure user can only update their own experience
        if serializer.instance.jobseeker_profile.user != self.request.user:
            raise serializers.ValidationError("You can only update your own experience records")
        serializer.save()
