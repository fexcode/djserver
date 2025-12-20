# xauth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "contrib_points", "is_staff"]
    list_editable = ["contrib_points"]

    fieldsets = list(BaseUserAdmin.fieldsets) + [
        ("扩展信息", {"fields": ("contrib_points",)}),
    ]
