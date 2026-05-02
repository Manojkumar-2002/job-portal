import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import CustomUser
from apps.users.serializers import LoginSerializer, RegisterSerializer, TOTPVerifySerializer, UserSerializer
from apps.users.services import TokenService, TOTPService
from apps.users.utils import REFRESH_COOKIE, delete_refresh_cookie, set_refresh_cookie

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("Register error: %s", str(e))
            raise


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]

            if not user.is_totp_enabled:
                TOTPService.enable_totp(user)
                uri = TOTPService.get_provisioning_uri(user)
                qr_code = TOTPService.generate_qr_base64(uri)
                return Response(
                    {
                        "message": "Credentials validated. TOTP has been set up, scan the QR and enter OTP to continue.",
                        "totp_required": True,
                        "email": user.email,
                        "qr_code": qr_code,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "message": "Credentials validated. Please enter your OTP to continue.",
                    "totp_required": True,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error("Login error: %s", str(e))
            raise


class TOTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = TOTPVerifySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                user = CustomUser.objects.get(email=serializer.validated_data["email"])
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            if not user.is_totp_enabled:
                return Response({"error": "TOTP not enabled"}, status=status.HTTP_400_BAD_REQUEST)

            otp_code = serializer.validated_data["otp_code"]
            bypass_otps = getattr(settings, "BYPASS_OTPS", [])

            is_valid = otp_code in bypass_otps or TOTPService.verify(user, otp_code)
            if not is_valid:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_401_UNAUTHORIZED)

            tokens = TokenService.create_tokens(user)
            response = Response(
                {"user": UserSerializer(user).data, "access_token": tokens["access_token"]},
                status=status.HTTP_200_OK,
            )
            return set_refresh_cookie(response, tokens["refresh_token"])
        except Exception as e:
            logger.error("TOTP verify error: %s", str(e))
            raise


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get(REFRESH_COOKIE)
            if not refresh_token:
                return Response({"error": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)

            tokens, error = TokenService.refresh_access_token(refresh_token)
            if error:
                return Response({"error": error}, status=status.HTTP_401_UNAUTHORIZED)

            return Response(tokens, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Token refresh error: %s", str(e))
            raise


class RevokeTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get(REFRESH_COOKIE)
            if not refresh_token:
                return Response({"error": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)

            revoked = TokenService.revoke_token(refresh_token)
            if not revoked:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
            return delete_refresh_cookie(response)
        except Exception as e:
            logger.error("Token revoke error: %s", str(e))
            raise


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(UserSerializer(request.user).data)
        except Exception as e:
            logger.error("Me view error: %s", str(e))
            raise
