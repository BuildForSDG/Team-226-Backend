from django.test import TestCase

from resources.models import Comment, Post, Category
from users.models import User


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user as comment owner
        user = User.objects.create(
            first_name="Big",
            last_name="Bob",
            username="bigbob",
            email="bigbob@test.com",
            password="secret",
        )

        category = Category.objects.create(name="Global warming", created_by=user)

        # Set up non-modified objects used by all test methods
        post = Post.objects.create(
            title="Green housing farming intro chapter 1",
            slug="green_housing_farming_intro_chapter_1",
            description="my test post",
            visibility="public",
            created_by=user,
            category=category,
        )

        Comment.objects.create(
            text="""Thanks for this chapter it help to solidify my
                knowledge on green house farming.""",
            created_by=user,
            post=post,
        )
