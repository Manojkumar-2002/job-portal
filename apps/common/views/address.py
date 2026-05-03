from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from apps.common.views.base_view import BaseAPIViewSet 
from apps.common.models import Address
from apps.common.serializers import AddressSerializer
from apps.profiles.models import EmployerProfile, JobSeekerProfile
from rest_framework.exceptions import ValidationError
from django.db import transaction
from apps.access_control.services.assign_role import assign_role_to_user

# ... (inside your AddressViewSet)

class AddressViewSet(BaseAPIViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Determine the source of truth
        is_employer_persona = self.request.is_employer
        is_jobseeker_persona = self.request.is_jobseeker

        if not (is_employer_persona or is_jobseeker_persona):
            raise ValidationError("You must be acting as an Employer or Job Seeker.")

        # 2. Bundle everything in a transaction for safety
        with transaction.atomic():
            # Save the address record first
            address = serializer.save()

            # 3. Create profile and assign role ONLY if this is the first time
            if is_employer_persona:
                profile, created = EmployerProfile.objects.get_or_create(
                    user=self.request.user,
                    defaults={"company_name": ""}
                )
                if created:
                    assign_role_to_user(self.request.user, 'employer')
            else:
                profile, created = JobSeekerProfile.objects.get_or_create(
                    user=self.request.user
                )
                if created:
                    assign_role_to_user(self.request.user, 'job_seeker')

            # 4. Link address
            profile.address = address
            profile.save()