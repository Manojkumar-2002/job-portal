from django.urls import path
from apps.users.views import LoginView, MeView, RefreshTokenView, RegisterView, RevokeTokenView, TOTPVerifyView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("totp/verify/", TOTPVerifyView.as_view(), name="totp-verify"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("token/revoke/", RevokeTokenView.as_view(), name="token-revoke"),
    path("me/", MeView.as_view(), name="me"),
]
