from rest_framework import viewsets, status
from ..utils.response_utils import ResponseHandler
from ..utils.serializer_utils import SerializerErrorHandler
from apps.profiles.models import JobSeekerProfile
from django.db import transaction
from apps.access_control.services.assign_role import assign_role_to_user

class BaseAPIViewSet(viewsets.ModelViewSet):
    """
    Universal Base: Only handles HTTP responses and error formatting.
    """
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ResponseHandler.error_response(
                message=SerializerErrorHandler.get_first_error_message(serializer.errors),
                errors=SerializerErrorHandler.format_errors(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        self.perform_create(serializer)
        return ResponseHandler.success_response("Created successfully", data=serializer.data, status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return ResponseHandler.error_response(
                message=SerializerErrorHandler.get_first_error_message(serializer.errors),
                errors=SerializerErrorHandler.format_errors(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        self.perform_update(serializer)
        return ResponseHandler.success_response("Updated successfully", data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ResponseHandler.success_response(message="Deleted successfully")




class BaseProfileViewSet(BaseAPIViewSet):
    """
    Entity-Specific Base: Adds profile auto-linking and role assignment logic.
    """
    def perform_create(self, serializer):
        with transaction.atomic():
            # 1. Get or Create the profile
            profile, created = JobSeekerProfile.objects.get_or_create(
                user=self.request.user
            )

            # 2. Trigger Role Assignment ONLY if this is the first time
            if created:
                assign_role_to_user(self.request.user, 'job_seeker')

            # 3. Save the actual record (Education/Experience/etc.) 
            # linked to this profile
            serializer.save(jobseeker_profile=profile)