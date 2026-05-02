from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "full_name", "is_totp_enabled", "is_active", "is_staff", "created_at"]
    list_filter = ["is_active", "is_staff", "is_totp_enabled"]
    search_fields = ["email", "full_name"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]

    fieldsets = (
        ("Credentials", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name",)}),
        ("TOTP", {"fields": ("is_totp_enabled",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_active", "is_staff"),
        }),
    )
