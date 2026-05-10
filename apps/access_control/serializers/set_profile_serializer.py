from rest_framework import serializers
from apps.profiles.models import EmployerProfile, JobSeekerProfile
from apps.common.constants import ProfileType

class SetPersonaSerializer(serializers.Serializer):
    persona = serializers.ChoiceField(choices=ProfileType.choices)

    # Centralized Mapping: Easy to add new personas later
    PROFILE_MAP = {
        ProfileType.EMPLOYER: EmployerProfile,
        ProfileType.JOB_SEEKER: JobSeekerProfile,
    }

    def validate(self, attrs):
        persona = attrs.get('persona')
        user = self.context['request'].user
        
        # Get the correct model from the map
        profile_model = self.PROFILE_MAP.get(persona)
        
        # Database Check
        if not profile_model.objects.filter(user=user).exists():
            raise serializers.ValidationError(f"You do not have an {persona} profile.")
        
        return attrs