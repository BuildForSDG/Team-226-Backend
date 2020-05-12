from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = (
        "email",
        "username",
        "phone_number",
        "profile_photo",
        "street",
        "city",
        "country",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "username",
        "phone_number",
        "profile_photo",
        "street",
        "city",
        "country",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "phone_number",
                    "profile_photo",
                    "street",
                    "city",
                    "country",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "phone_number",
                    "profile_photo",
                    "street",
                    "city",
                    "country",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
