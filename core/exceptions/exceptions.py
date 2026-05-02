import logging
import traceback

from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            "error": True,
            "status_code": response.status_code,
            "message": _extract_message(response.data),
        }

        if isinstance(exc, ValidationError):
            error_data["message"] = _extract_message(response.data)
        elif isinstance(exc, NotAuthenticated):
            error_data["message"] = "Authentication credentials were not provided."
        elif isinstance(exc, AuthenticationFailed):
            error_data["message"] = "Invalid authentication credentials."
        elif isinstance(exc, PermissionDenied):
            error_data["message"] = "You do not have permission to perform this action."
        elif isinstance(exc, Throttled):
            error_data["message"] = f"Request was throttled. Try again in {exc.wait} seconds."

        response.data = error_data

    return response


def _extract_message(data):
    if isinstance(data, dict):
        messages = []
        for key, value in data.items():
            if key == "non_field_errors":
                messages.extend(value if isinstance(value, list) else [value])
            else:
                messages.append(f"{key}: {value[0] if isinstance(value, list) else value}")
        return " | ".join(str(m) for m in messages)
    if isinstance(data, list):
        return " | ".join(str(i) for i in data)
    return str(data)


class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(
            "Unhandled exception: %s\n%s",
            str(exception),
            traceback.format_exc(),
        )
        return JsonResponse(
            {
                "error": True,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An unexpected error occurred. Please try again later.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
