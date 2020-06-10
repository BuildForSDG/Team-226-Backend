from django.test import TestCase

from resources.models import List
from users.models import User


class ListModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user as list owner
        user = User.objects.create(
            first_name="Big",
            last_name="Bob",
            username="bigbob",
            email="bigbob@test.com",
            password="secret",
        )

        # Set up non-modified objects used by all test methods
        List.objects.create(
            title="Green housing farming intro",
            description="my test list",
            visibility="public",
            created_by=user,
        )

    def test_title_label(self):
        test_list = List.objects.first()
        field_label = test_list._meta.get_field("title").verbose_name
        assert field_label == "List title"

    def test_title_max_length(self):
        test_list = List.objects.first()
        max_length = test_list._meta.get_field("title").max_length
        assert max_length == 255

    def test_object_title_is_valid(self):
        test_list = List.objects.first()
        expected_object_title = f"{test_list.title}"
        assert expected_object_title == str(test_list)

    def test_description_label(self):
        test_list = List.objects.first()
        field_label = test_list._meta.get_field("description").verbose_name
        assert field_label == "Description of the List"

    def test_cover_image_label(self):
        test_list = List.objects.first()
        field_label = test_list._meta.get_field("cover_image").verbose_name
        assert field_label == "Cover image"

    def test_visibility_label(self):
        test_list = List.objects.first()
        field_label = test_list._meta.get_field("visibility").verbose_name
        assert field_label == "Visible to"

    def test_visibility_max_length(self):
        test_list = List.objects.first()
        max_length = test_list._meta.get_field("visibility").max_length
        assert max_length == 30
