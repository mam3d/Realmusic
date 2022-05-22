from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "is_staff", "is_admin"]
    list_display_links = ('username', 'email')
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ["username", "email"]
    fieldsets = (
        (None, {
            "fields": (
                "username",
                "email",
                "password",
                "is_staff",
                "is_admin",
                "is_superuser",
            ),
        }),
        ("Permissions", {
            "fields": (
                "groups",
            ),
        }),
    )
    
