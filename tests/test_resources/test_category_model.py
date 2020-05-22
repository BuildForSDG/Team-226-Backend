from django.test import TestCase

from resources.models import Category
from users.models import User


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(email="bob@gmail.com", password="bob")
        Category.objects.create(name="Green House", slug="green-house", created_by=user)

    def test_name_label(self):
        category = Category.objects.first()
        field_label = category._meta.get_field("name").verbose_name
        assert field_label == "Category name"

    def test_name_max_length(self):
        category = Category.objects.first()
        max_length = category._meta.get_field("name").max_length
        print(max_length)
        assert max_length == 155

    def test_slug_label(self):
        category = Category.objects.first()
        field_label = category._meta.get_field("slug").verbose_name
        assert field_label == "Category slug(from name)"

    def test_slug_max_length(self):
        category = Category.objects.first()
        max_length = category._meta.get_field("slug").max_length
        print(max_length)
        assert max_length == 255

    def test_object_name_is_valid(self):
        category = Category.objects.first()
        expected_object_name = f"{category.name}"
        assert expected_object_name == str(category)
