from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Student, Self
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    search_fields = ("email", "fullname", "username")
    ordering = ("-id",)
    filter_horizontal = ("user_permissions", "groups")

    list_display = (
        "email",
        "fullname",
        "username",
        "is_active",
        "is_admin",
        "is_ban",
    )
    list_filter = ("is_active", "is_admin", "is_ban")
    readonly_fields = ("jlast_login",)

    fieldsets = (
        (
            None,
            {
                "fields": ("email", "fullname"),
            },
        ),
        (
            "دسترسی ها",
            {
                "fields": (
                    "is_active",
                    "is_ban",
                    "is_admin",
                    "is_superuser",
                    "jlast_login",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("email", "fullname", "username", "password1", "password2"),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            superuser_field = form.base_fields.get("is_superuser")
            if superuser_field:
                superuser_field.disabled = True
            admin_field = form.base_fields.get("is_admin")
            if admin_field:
                admin_field.disabled = True
        return form


class StudentAdmin(admin.ModelAdmin):
    search_fields = ("user", "university__name", "student_id")
    ordering = (
        "-id",
        "-user__created_at",
    )

    list_display = (
        "user",
        "university",
        "student_id",
        "has_dormitory",
    )
    list_filter = ("has_dormitory",)


class SelfsAdmin(admin.ModelAdmin):
    search_fields = ("name", "code", "address")
    ordering = ("-code",)

    list_display = (
        "name",
        "code",
        "address",
        "is_active",
    )
    list_filter = ("is_active",)


admin.site.register(Student, StudentAdmin)
admin.site.register(Self, SelfsAdmin)
admin.site.register(User, UserAdmin)
