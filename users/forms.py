from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        """ user change form meta properties """

        model = User
        fields = (
            "email",
            "username",
            "is_superuser",
            "first_name",
            "last_name",
            "street",
            "city",
            "country",
            "profile_photo",
            "phone_number",
            "pref_contact_method",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        """ user change form meta properties """

        model = User
        fields = (
            "email",
            "username",
            "is_superuser",
            "first_name",
            "last_name",
            "street",
            "city",
            "country",
            "profile_photo",
            "phone_number",
            "pref_contact_method",
        )
