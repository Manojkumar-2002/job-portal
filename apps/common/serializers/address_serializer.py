from rest_framework import serializers
from apps.common.models import Address
from ..constants import ProfileType


class AddressSerializer(serializers.ModelSerializer):
    profile_type = serializers.ChoiceField(
        ProfileType.choices, write_only=True, required=True
    )

    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "city",
            "state",
            "country",
            "postal_code",
            "profile_type",
        ]
        read_only_fields = ["id"]

