from django.test import TestCase

from resources.models import Category, Post
from users.models import User


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user as post owner
        user = User.objects.create(
            first_name="Big",
            last_name="Bob",
            username="bigbob",
            email="bigbob@test.com",
            password="secret",
        )

        # create a category
        category = Category.objects.create(name="fertilizers", created_by=user)

        # Set up non-modified objects used by all test methods
        Post.objects.create(
            title="Green housing farming intro chapter 1",
            slug="green_housing_farming_intro_chapter_1",
            description="my test post",
            visibility="public",
            created_by=user,
            category=category,
        )

    def test_title_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field("title").verbose_name
        assert field_label == "Post title"

    def test_title_max_length(self):
        post = Post.objects.first()
        max_length = post._meta.get_field("title").max_length
        assert max_length == 200

    def test_object_title_is_valid(self):
        post = Post.objects.first()
        expected_object_title = f"{post.title}"
        assert expected_object_title == str(post)

    def test_slug_label(self):
        category = Post.objects.first()
        field_label = category._meta.get_field("slug").verbose_name
        assert field_label == "Post slug(from title)"

    def test_slug_max_length(self):
        category = Post.objects.first()
        max_length = category._meta.get_field("slug").max_length
        assert max_length == 255

    def test_description_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field("description").verbose_name
        assert field_label == "Description of the post"

    def test_video_link_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field("video_link").verbose_name
        assert field_label == "Post video link"

    def test_visibility_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field("visibility").verbose_name
        assert field_label == "Visible to"

    def test_visibility_max_length(self):
        post = Post.objects.first()
        max_length = post._meta.get_field("visibility").max_length
        assert max_length == 30

    def test_post_user(self):
        post = Post.objects.first()
        assert post.created_by.username == "bigbob"
