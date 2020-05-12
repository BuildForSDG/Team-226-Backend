from django.test import TestCase

from resources.models import Comment, Post
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

        # Set up non-modified objects used by all test methods
        post = Post.objects.create(
            title="Green housing farming intro chapter 1",
            slug="green_housing_farming_intro_chapter_1",
            description="my test post",
            images="['test_post_image1.png', 'test_post_image2.png']",
            visibility="public",
            user=user,
        )

        Comment.objects.create(
            text="""Thanks for this chapter it help to solidify my
                knowledge on green house farming.""",
            image="test_post_image1.png",
            user=user,
            post=post,
        )

    def test_text_label(self):
        comment = Comment.objects.first()
        field_label = comment._meta.get_field("text").verbose_name
        assert field_label == "Comment text"

    def test_object_text_is_valid(self):
        comment = Comment.objects.first()
        expected_object_text = f"{comment.text}"
        assert expected_object_text == str(comment)

    def test_image_label(self):
        comment = Comment.objects.first()
        field_label = comment._meta.get_field("image").verbose_name
        assert field_label == "Comment image"

    def test_comment_post(self):
        comment = Comment.objects.first()
        assert comment.post.slug == "green_housing_farming_intro_chapter_1"

    def test_comment_user(self):
        comment = Comment.objects.first()
        assert comment.user.username == "bigbob"
