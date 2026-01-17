from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
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