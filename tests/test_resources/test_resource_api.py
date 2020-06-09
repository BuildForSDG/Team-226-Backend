from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from resources.models import Category, Comment, Land, List, Post
from tests.helpers import TestSetupData
from users.models import User


class TestResourcesApi(APITestCase):
    def setUp(self) -> None:
        self.client.post(reverse("users:user-register"), data=TestSetupData.REGISTER)
        self.client.post(reverse("user-login"), TestSetupData.LOGIN)
        self.user = User.objects.first()
        TestSetupData.CATEGORY_CREATE["created_by_id"] = self.user.id
        self.category = Category.objects.create(**TestSetupData.CATEGORY_CREATE)
        TestSetupData.POST_CREATE.update(
            {"category_id": self.category.id, "created_by_id": self.user.id}
        )
        TestSetupData.LEASE_LAND_CREATE["owner_id"] = self.user.id
        self.land = Land.objects.create(**TestSetupData.LEASE_LAND_CREATE)
        self.post = Post.objects.create(**TestSetupData.POST_CREATE)
        TestSetupData.LIST_CREATE["created_by_id"] = self.user.id
        self.listing = List.objects.create(**TestSetupData.LIST_CREATE)
        TestSetupData.COMMENT_CREATE["created_by_id"] = self.user.id
        TestSetupData.COMMENT_CREATE["post_id"] = self.post.id
        self.comment = Comment.objects.create(**TestSetupData.COMMENT_CREATE)

    def test_upload_images(self):
        data = {
            "upload_for": self.post.id,
            "images": [
                TestSetupData.temporary_image(),
                TestSetupData.temporary_image(),
            ],
        }
        response = self.client.post(
            reverse("resources:upload_images", kwargs={"type": "post"}),
            data,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_save_category(self):
        response = self.client.post(
            reverse("resources:create_or_get_categories"), TestSetupData.CATEGORY
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_category(self):
        response = self.client.get(reverse("resources:create_or_get_categories"))
        assert response.status_code == status.HTTP_200_OK

    def test_create_free_land(self):
        response = self.client.post(
            reverse("resources:create_or_get_lands"), TestSetupData.FREE_LAND
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_lease_land(self):
        response = self.client.post(
            reverse("resources:create_or_get_lands"), TestSetupData.LEASE_LAND
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_lease_land_without_cost(self):
        response = self.client.post(
            reverse("resources:create_or_get_lands"),
            TestSetupData.LEASE_LAND_WITHOUT_COST,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_lease_land_without_periodicity(self):
        response = self.client.post(
            reverse("resources:create_or_get_lands"),
            TestSetupData.LEASE_LAND_WITHOUT_PERIODICITY,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_land(self):
        response = self.client.delete(
            reverse("resources:update_land", kwargs={"land_id": self.land.id})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_user_land(self):
        response = self.client.get(reverse("resources:get_lands"))
        assert response.status_code == status.HTTP_200_OK

    def test_create_free_list(self):
        response = self.client.post(
            reverse("resources:create_or_get_list"), TestSetupData.LIST
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_list(self):
        response = self.client.delete(
            reverse("resources:update_list", kwargs={"list_id": self.listing.id})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_user_list(self):
        response = self.client.get(reverse("resources:get_list"))
        assert response.status_code == status.HTTP_200_OK

    def test_create_post(self):
        TestSetupData.POST["created_by"] = self.user.id
        TestSetupData.POST["category"] = self.category.id
        response = self.client.post(
            reverse("resources:create_or_get_post"), TestSetupData.POST
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_delete_post(self):
        response = self.client.delete(
            reverse("resources:update_post", kwargs={"post_id": self.post.id})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_user_post(self):
        response = self.client.get(reverse("resources:get_posts"))
        assert response.status_code == status.HTTP_200_OK

    def test_list_add_post(self):
        response = self.client.post(
            reverse("resources:add_post_to_list"),
            {"list": self.listing.id, "post": self.post.id},
        )
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_list_remove_post(self):
        response = self.client.delete(
            reverse("resources:delete_post_from_list"),
            {"list": self.listing.id, "post": self.post.id},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_fail_remove_post(self):
        response = self.client.delete(
            reverse("resources:delete_post_from_list"), {"list": 2, "post": 2}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_comment_on_post(self):
        response = self.client.post(
            reverse("resources:comment", kwargs={"post_id": self.post.id}),
            {"text": "Test comment"},
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_reply_on_comment(self):
        response = self.client.post(
            reverse("resources:comment", kwargs={"post_id": self.post.id}),
            {"text": "First Reply", "reply_to": self.comment.id},
        )
        assert response.status_code == status.HTTP_201_CREATED
