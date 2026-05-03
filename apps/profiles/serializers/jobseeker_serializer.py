from rest_framework import serializers
from apps.profiles.models import (
    JobSeekerProfile,
    JobSeekerEducation,
    JobSeekerExperience,
)
from apps.common.models import Address
from apps.common.serializers import AddressSerializer
from apps.users.models import CustomUser


class JobSeekerEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerEducation
        fields = [
            "id",
            "institution",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "is_current",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class JobSeekerExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerExperience
        fields = [
            "id",
            "company_name",
            "job_title",
            "location",
            "start_date",
            "end_date",
            "is_current",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source="address", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = JobSeekerProfile
        fields = [
            "id",
            "user",
            "bio",
            "date_of_birth",
            "gender",
            "phone",
            "address",
            "address_id",
            "experience_years",
            "skills",
            "resume",
            "linkedin_url",
            "portfolio_url",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class JobSeekerProfileDetailSerializer(serializers.ModelSerializer):
    educations = JobSeekerEducationSerializer(many=True, read_only=True)
    experiences = JobSeekerExperienceSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    user_full_name = serializers.CharField(source="user.full_name", read_only=True)
    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source="address", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = JobSeekerProfile
        fields = [
            "id",
            "user",
            "user_email",
            "user_full_name",
            "bio",
            "date_of_birth",
            "gender",
            "phone",
            "address",
            "address_id",
            "experience_years",
            "skills",
            "resume",
            "linkedin_url",
            "portfolio_url",
            "is_available",
            "educations",
            "experiences",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "educations", "experiences", "created_at", "updated_at"]
