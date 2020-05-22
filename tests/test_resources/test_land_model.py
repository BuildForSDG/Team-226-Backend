from django.test import TestCase

from resources.models import Land
from users.models import User


class LandModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user as land owner
        user = User.objects.create(
            first_name="Big",
            last_name="Bob",
            username="bigbob",
            email="bigbob@test.com",
            password="secret",
        )

        # Set up non-modified objects used by all test methods
        Land.objects.create(
            title="5022 in Bonji",
            cost=500,
            for_type="for rent",
            size=50,
            size_unit_measurement="M",
            location="Bonji, South West, Cameroon",
            visibility="public",
            owner=user,
        )

    def test_title_label(self):
        land = Land.objects.first()
        field_label = land._meta.get_field("title").verbose_name
        assert field_label == "Land title"

    def test_title_max_length(self):
        land = Land.objects.first()
        max_length = land._meta.get_field("title").max_length
        print(max_length)
        assert max_length == 255

    def test_object_title_is_valid(self):
        land = Land.objects.first()
        expected_object_title = f"{land.title}"
        assert expected_object_title == str(land)

    def test_cost_label(self):
        land = Land.objects.first()
        field_label = land._meta.get_field("cost").verbose_name
        assert field_label == "Cost of land"

    def test_size_label(self):
        land = Land.objects.first()
        field_label = land._meta.get_field("size").verbose_name
        assert field_label == "Land size"

    def test_size_type_label(self):
        land = Land.objects.first()
        field_label = land._meta.get_field("size_unit_measurement").verbose_name
        assert field_label == "Land size measurement type"

    def test_size_type_max_length(self):
        land = Land.objects.first()
        max_length = land._meta.get_field("size_unit_measurement").max_length
        print(max_length)
        assert max_length == 30

    def test_for_type_label(self):
        land = Land.objects.first()
        field_label = land._meta.get_field("for_type").verbose_name
        assert field_label == "Land listing type(free or rent)"

    def test_for_type_max_length(self):
        land = Land.objects.first()
        max_length = land._meta.get_field("for_type").max_length
        print(max_length)
        assert max_length == 30

    def test_location_label(self):
        land = Land.objects.first()
        field_label = land._meta.get_field("location").verbose_name
        assert field_label == "Land location"

    def test_location_max_length(self):
        land = Land.objects.first()
        max_length = land._meta.get_field("location").max_length
        print(max_length)
        assert max_length == 255

    def test_visibility_label(self):
        land = Land.objects.first()
        field_label = land._meta.get_field("visibility").verbose_name
        assert field_label == "Visible to"

    def test_visibility_max_length(self):
        land = Land.objects.first()
        max_length = land._meta.get_field("visibility").max_length
        print(max_length)
        assert max_length == 30
