from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    list_display = ("email", "is_staff")
    list_display_links = ("email",)
    list_filter = ("is_staff",)
    readonly_fields = ("pubkey",)
    fieldsets = (
        ("Credentials", {"fields": ("email", "password", "pubkey")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
