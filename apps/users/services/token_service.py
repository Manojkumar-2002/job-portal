import logging
import secrets
from datetime import timedelta

from django.utils import timezone
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings

logger = logging.getLogger(__name__)


class TokenService:

    @staticmethod
    def _get_app():
        from django.conf import settings
        client_id = settings.OAUTH2_CLIENT_ID
        try:
            return Application.objects.get(client_id=client_id)
        except Application.DoesNotExist:
            raise ValueError(f"OAuth2 Application with client_id '{client_id}' not found")

    @staticmethod
    def create_tokens(user):
        try:
            app = TokenService._get_app()
            RefreshToken.objects.filter(user=user, application=app).delete()

            refresh_token = RefreshToken.objects.create(
                user=user,
                token=secrets.token_urlsafe(32),
                application=app,
            )
            access_token = AccessToken.objects.create(
                user=user,
                token=secrets.token_urlsafe(32),
                application=app,
                expires=timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
                scope="read write",
                source_refresh_token=refresh_token,
            )
            return {
                "access_token": access_token.token,
                "refresh_token": refresh_token.token,
                "token_type": "Bearer",
            }
        except Exception as e:
            logger.error("Token creation failed: %s", str(e))
            raise

    @staticmethod
    def refresh_access_token(refresh_token_value):
        try:
            refresh_token = RefreshToken.objects.select_related("user", "application").get(
                token=refresh_token_value
            )
        except RefreshToken.DoesNotExist:
            return None, "Invalid refresh token"
        except Exception as e:
            logger.error("Token refresh failed: %s", str(e))
            raise

        try:
            AccessToken.objects.filter(source_refresh_token=refresh_token).delete()
            access_token = AccessToken.objects.create(
                user=refresh_token.user,
                token=secrets.token_urlsafe(32),
                application=refresh_token.application,
                expires=timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
                scope="read write",
                source_refresh_token=refresh_token,
            )
            return {"access_token": access_token.token, "token_type": "Bearer"}, None
        except Exception as e:
            logger.error("Access token creation during refresh failed: %s", str(e))
            raise

    @staticmethod
    def revoke_token(refresh_token_value):
        try:
            refresh_token = RefreshToken.objects.get(token=refresh_token_value)
            AccessToken.objects.filter(source_refresh_token=refresh_token).delete()
            refresh_token.delete()
            return True
        except RefreshToken.DoesNotExist:
            return False
        except Exception as e:
            logger.error("Token revocation failed: %s", str(e))
            raise
