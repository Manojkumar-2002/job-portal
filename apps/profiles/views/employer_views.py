from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.profiles.models import EmployerProfile
from apps.profiles.serializers import (
    EmployerProfileSerializer,
    EmployerProfileDetailSerializer,
)


class EmployerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for Employer Profile management"""

    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EmployerProfileDetailSerializer
        return EmployerProfileSerializer

    def get_queryset(self):
        # Users can only see their own profile or admins can see all
        if self.request.user.is_staff:
            return EmployerProfile.objects.all()
        return EmployerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current authenticated user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure user can only update their own profile
        if serializer.instance.user != self.request.user:
            raise serializers.ValidationError("You can only update your own profile")
        serializer.save()


