from rest_framework import serializers
from apps.profiles.models import EmployerProfile
from apps.common.models import Address
from apps.common.serializers import AddressSerializer
from apps.users.models import CustomUser


class EmployerProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source="address", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = EmployerProfile
        fields = [
            "id",
            "user",
            "company_name",
            "company_logo",
            "company_website",
            "company_description",
            "industry",
            "company_size",
            "address",
            "address_id",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class EmployerProfileDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    user_full_name = serializers.CharField(source="user.full_name", read_only=True)
    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), source="address", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = EmployerProfile
        fields = [
            "id",
            "user",
            "user_email",
            "user_full_name",
            "company_name",
            "company_logo",
            "company_website",
            "company_description",
            "industry",
            "company_size",
            "address",
            "address_id",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "user_email",
            "user_full_name",
            "created_at",
            "updated_at",
        ]
