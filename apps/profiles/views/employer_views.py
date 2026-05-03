from rest_framework.permissions import IsAuthenticated
from apps.common.views import BaseAPIViewSet 
from apps.profiles.models import EmployerProfile
from apps.profiles.serializers import (
    EmployerProfileSerializer, 
    EmployerProfileDetailSerializer
)
from apps.common.permissions import IsOwner, IsEmployer
    
from django.db import transaction
from apps.access_control.services.assign_role import assign_role_to_user

class EmployerProfileViewSet(BaseAPIViewSet):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsEmployer]

    def get_serializer_class(self):
        # Use Detail serializer for fetching full profile, otherwise default
        if self.action == "retrieve":
            return EmployerProfileDetailSerializer
        return EmployerProfileSerializer

    def get_queryset(self):
        # Optimized: filter by owner, and join related user/address fields
        # Add prefetch_related for any other relations (e.g., 'jobs')
        return EmployerProfile.objects.filter(
            user=self.request.user
        ).select_related('user', 'address') 


    def perform_create(self, serializer):
        with transaction.atomic():
            # 1. Save the profile and link to the user
            # serializer.save() returns the instance created
            profile = serializer.save(user=self.request.user)
            
            # 2. Assign the 'employer' role to the user
            # The service handles idempotency (get_or_create) internally
            assign_role_to_user(self.request.user, 'employer')

    def perform_update(self, serializer):
        serializer.save()