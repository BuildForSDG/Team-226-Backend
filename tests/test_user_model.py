from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up group with perms
        group = Group.objects.create(name="app_user")
        change_user_permissions = Permission.objects.filter(
            codename__in=["change_user", "view_user"],
        )
        group.permissions.add(*change_user_permissions)

        # Set up non-modified objects used by all test methods

        user = User.objects.create(
            first_name="Big",
            last_name="Bob",
            username="bigbob",
            email="bigbob@test.com",
            password="secret",
        )

        # category1 = Category.objects.create(name="horticulture")
        # category2 = Category.objects.create(name="green-house")

        user.groups.add(group)
        # user.pref_categories.add(category1, category2)

    def test_email_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("email").verbose_name
        assert field_label == "email address"

    def test_email_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("email").max_length
        assert max_length == 255

    def test_first_name_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("first_name").verbose_name
        assert field_label == "first name"

    def test_first_name_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("first_name").max_length
        assert max_length == 30

    def test_last_name_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("last_name").verbose_name
        assert field_label == "last name"

    def test_last_name_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("last_name").max_length
        assert max_length == 150

    def test_username_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("username").verbose_name
        assert field_label == "username"

    def test_username_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("username").max_length
        assert max_length == 150

    def test_object_name_is_last_name_comma_first_name(self):
        user = User.objects.first()
        expected_object_name = f"{user.last_name}, {user.first_name}"
        assert expected_object_name == str(user)

    def test_get_absolute_url(self):
        user = User.objects.first()
        # This will also fail if the urlconf is not defined.
        assert user.get_absolute_url() == "/users/user/" + user.username

    def test_should_not_check_unusable_password(self):
        user = User.objects.first()
        assert user.check_password("secret") is False

    def test_user_is_in_app_user_group(self):
        user = User.objects.first()
        assert user.groups.filter(name="app_user").exists()

    def test_date_created_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("date_created").verbose_name
        assert field_label == "date created"

    def test_date_updated_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("date_updated").verbose_name
        assert field_label == "date updated"

    def test_phone_number_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("phone_number").max_length
        assert max_length == 80

    def test_profile_photo_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("profile_photo").verbose_name
        assert field_label == "Profile picture"

    def test_street_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("street").max_length
        assert max_length == 150

    def test_city_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("city").max_length
        assert max_length == 150

    def test_country_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("country").max_length
        assert max_length == 150

    def test_pref_contact_method_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("pref_contact_method").verbose_name
        assert field_label == "Preferential Contact Method"
