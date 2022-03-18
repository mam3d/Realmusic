from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username","is_staff","is_admin"]
    list_filter = ("is_staff", "is_superuser", "groups")
