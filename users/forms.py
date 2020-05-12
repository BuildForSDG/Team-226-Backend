from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "email",
            "username",
            "phone_number",
            "profile_photo",
            "street",
            "city",
            "country",
        )


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = (
            "email",
            "username",
            "phone_number",
            "profile_photo",
            "street",
            "city",
            "country",
        )
