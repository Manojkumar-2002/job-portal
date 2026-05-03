from django.db.models import Q
from rest_framework import status, viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.models import Address
from apps.common.serializers import AddressSerializer
from apps.profiles.models import EmployerProfile, JobSeekerProfile
from ..constants import ProfileType


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Address.objects.all()
        return Address.objects.filter(
            Q(jobseeker_profile__user=self.request.user)
            | Q(employer_profile__user=self.request.user)
        ).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        address = serializer.instance

        profile_type = serializer.validated_data.get("profile_type")
        profile = self._get_profile(profile_type, request.user)
        profile.address = address
        profile.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _get_profile(self, profile_type, user):
        if profile_type == ProfileType.JOB_SEEKER:
            profile, _ = JobSeekerProfile.objects.get_or_create(user=user)
        else:
            profile, _ = EmployerProfile.objects.get_or_create(
                user=user,
                defaults={"company_name": ""},
            )

        return profile