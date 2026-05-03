from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

# Standardized Response Handler
from apps.common.utils.response_utils import ResponseHandler
from apps.profiles.models import EmployerProfile, JobSeekerProfile
from apps.users.serializers import LoginSerializer, RegisterSerializer, TOTPVerifySerializer, UserSerializer
from apps.users.services import TokenService, TOTPService
from apps.users.utils import REFRESH_COOKIE, delete_refresh_cookie, set_refresh_cookie
from django.conf import settings

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return ResponseHandler.success_response(
            message = "Registration successful",
            data={"user": UserSerializer(user).data},
            status_code=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        response_data = {"email": user.email, "totp_required": True}
        
        # Handle TOTP setup if not enabled
        if not user.is_totp_enabled:
            TOTPService.enable_totp(user)
            uri = TOTPService.get_provisioning_uri(user)
            response_data["qr_code"] = TOTPService.generate_qr_base64(uri)
            message= "TOTP set up. Scan QR to continue."
        else:
            message = "Please enter your OTP to continue."

        return ResponseHandler.success_response(data=response_data, message=message)


class TOTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Validate (Handles User lookup and OTP structural validation)
        serializer = TOTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data["user"]
        otp_code = serializer.validated_data["otp_code"]
        bypass_otps = getattr(settings, "BYPASS_OTPS", [])

        # 2. Verify OTP
        if otp_code not in bypass_otps and not TOTPService.verify(user, otp_code):
            return ResponseHandler.error_response(
                message="Invalid OTP", 
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # 3. Create Tokens
        tokens = TokenService.create_tokens(user)

        # 4. State Hydration: Check for existing profiles to guide the frontend
        has_employer = EmployerProfile.objects.filter(user=user).exists()
        has_jobseeker = JobSeekerProfile.objects.filter(user=user).exists()

        # 5. Success Response
        response = ResponseHandler.success_response(
            message="Login successful",
            data={
                "user": UserSerializer(user).data,
                "access_token": tokens["access_token"],
                "user_context": {  # Hydrate frontend with role status
                    "has_employer": has_employer,
                    "has_jobseeker": has_jobseeker,
                }
            }
        )
        
        # 6. Set HttpOnly Refresh Cookie
        return set_refresh_cookie(response, tokens["refresh_token"])


class AuthStatusView(APIView):
    """
    Returns the current user's profile and state context.
    Used by the frontend to re-hydrate state on page refresh.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Check profile status (Same logic as login)
        has_employer = EmployerProfile.objects.filter(user=user).exists()
        has_jobseeker = JobSeekerProfile.objects.filter(user=user).exists()

        return ResponseHandler.success_response(
            message="User status retrieved",
            data={
                "user": UserSerializer(user).data,
                "user_context": {
                    "has_employer": has_employer,
                    "has_jobseeker": has_jobseeker,
                }
            }
        )

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)
        if not refresh_token:
            return ResponseHandler.error_response(message="Refresh token not found", status_code=status.HTTP_400_BAD_REQUEST)

        tokens, error = TokenService.refresh_access_token(refresh_token)
        if error:
            return ResponseHandler.error_response(message=error, status_code=status.HTTP_401_UNAUTHORIZED)

        return ResponseHandler.success_response(data=tokens)

class RevokeTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)
        if not refresh_token:
            return ResponseHandler.error_response(message="Refresh token not found", status_code=status.HTTP_400_BAD_REQUEST)

        if not TokenService.revoke_token(refresh_token):
            return ResponseHandler.error_response(message="Invalid refresh token", status_code=status.HTTP_400_BAD_REQUEST)

        response = ResponseHandler.success_response(message="Logged out successfully")
        return delete_refresh_cookie(response)