from dj_rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_framework import serializers

from zero_hunger import settings

from .models import User


class LoginSerializer(RestAuthLoginSerializer):
    username = None


class UserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
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
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "profile_photo": {"required": False},
        }


class UserSerializerWithToken(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password"
    )
    profile_photo = serializers.CharField(required=False)
    token = serializers.SerializerMethodField()

    def get_token(self, object):
        jwt_payload_handler = settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(object)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        print(validated_data)
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."}
            )
        if password != password2:
            raise serializers.ValidationError({"password": "The two passwords differ."})

        del validated_data["password2"]

        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            "email",
            "token",
            "username",
            "password",
            "password2",
            "is_superuser",
            "first_name",
            "last_name",
            "street",
            "city",
            "country",
            "profile_photo",
            "phone_number",
            "pref_contact_method",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "profile_photo": {"required": False},
        }
