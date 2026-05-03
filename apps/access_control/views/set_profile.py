from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.common.utils.response_utils import ResponseHandler
from ..serializers import SetPersonaSerializer

class SetPersonaView(APIView):
    """
    Sets the user's active persona and sets a secure HttpOnly cookie.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Validate: Serializer handles the DB check & permission check
        serializer = SetPersonaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # 2. Extract the validated persona
        persona = serializer.validated_data['persona']

        # 3. Create the Response
        response = ResponseHandler.success_response(
            message=f"Successfully switched to {persona}"
        )
        
        # 4. Set the HttpOnly Cookie
        # This cookie is now the "source of truth" for your Middleware
        response.set_cookie(
            'active_persona',
            persona,
            httponly=True,  # Prevent JS access
            secure=True,    # Ensure HTTPS
            samesite='Lax', # CSRF protection
            max_age=3600 * 24 * 7 # 7 days
        )
        
        return response