import base64
import logging
from io import BytesIO

import pyotp
import qrcode

logger = logging.getLogger(__name__)


class TOTPService:

    @staticmethod
    def generate_secret():
        return pyotp.random_base32()

    @staticmethod
    def get_provisioning_uri(user):
        try:
            totp = pyotp.TOTP(user.totp_secret)
            return totp.provisioning_uri(name=user.email, issuer_name="JobPortal")
        except Exception as e:
            logger.error("Failed to generate TOTP provisioning URI: %s", str(e))
            raise

    @staticmethod
    def generate_qr_base64(uri):
        try:
            qr = qrcode.make(uri)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)
            return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            logger.error("Failed to generate QR code: %s", str(e))
            raise

    @staticmethod
    def verify(user, otp_code):
        try:
            if not user.totp_secret:
                return False
            totp = pyotp.TOTP(user.totp_secret)
            return totp.verify(otp_code, valid_window=1)
        except Exception as e:
            logger.error("TOTP verification failed: %s", str(e))
            raise

    @staticmethod
    def enable_totp(user):
        try:
            secret = TOTPService.generate_secret()
            user.totp_secret = secret
            user.is_totp_enabled = True
            user.save(update_fields=["_totp_secret", "is_totp_enabled"])
            return secret
        except Exception as e:
            logger.error("Failed to enable TOTP: %s", str(e))
            raise
