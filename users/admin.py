from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "avatar_preview",
        "email",
        "name",
        "surname",
        "projects_count",
        "is_staff",
    )
    search_fields = ("email", "name", "surname")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "name",
                    "surname",
                    "avatar",
                    "phone",
                    "github_url",
                    "about",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "surname",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    @admin.display(description="Аватар")
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url,
            )
        return format_html(
            '<div style="width:40px; height:40px; background:#667eea; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white;">{}</div>',
            obj.name[0].upper() if obj.name else "?",
        )

    @admin.display(description="Проекты")
    def projects_count(self, obj):
        count = obj.participated_projects.count()
        return count
