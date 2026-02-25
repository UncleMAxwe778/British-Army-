from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    ordering = ("email",)

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "rank",
        "regiment",
        "is_active",
        "is_staff"
    )
    list_editable = (
        "rank",
        "regiment",
        "is_active",
        "is_staff"
    )