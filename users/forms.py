from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
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


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
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
