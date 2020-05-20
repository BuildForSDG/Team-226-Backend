import pytest
from rest_framework.test import APITestCase
from rest_framework.views import status

from users.models import User

# from users.serializers import UserSerializer


# test case for the user model
class TestUserAPI(APITestCase):
    user_detail = "/api/user/"

    def setUp(self):
        """
            get both the access and refresh tokens
        """
        # create a new user making a post request to djoser endpoint
        self.data = {
            "email": "test@test.com",
            "password": "secret",
            "password2": "secret",
            "first_name": "test",
            "last_name": "user",
        }
        self.user = self.client.post("/api/auth/register/", data=self.data)

        # obtain a json web token for the newly created user
        del self.data["password2"]
        response = self.client.post("/api/auth/token/", data=self.data)

        self.token = response.data["access"]
        self.set_api_auth_header()

    def set_api_auth_header(self):
        """
            Sets the authorization header
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    @pytest.mark.run(order=1)
    def test_get_user_details_unauthorized(self):
        """
            Retrieve user without the authorization header
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer ")
        self.client.force_authenticate(user=None)

        user = User.objects.first()
        url = self.user_detail + str(user.pk) + "/"

        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.run(order=2)
    def test_get_user_details_authorized(self):
        """
            Retrieve user with the authorization header set
        """
        self.set_api_auth_header()
        user = User.objects.first()
        url = self.user_detail + str(user.pk) + "/"

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.run(order=3)
    def test_full_update_user_details(self):
        """
            Does a full update of the user details
        """
        self.set_api_auth_header()
        user = User.objects.first()
        url = self.user_detail + str(user.pk) + "/"

        self.data = {
            "email": "test1@test.com",
            "username": "test1-user1",
            "street": "Malingo",
            "city": "Buea",
            "country": "Cameroon",
            "is_superuser": False,
            "first_name": "test1",
            "last_name": "user",
            "profile_photo": "/user_photos/test_img.png",
            "phone_number": "2839238492",
            "pref_contact_method": "PH",
        }
        response = self.client.put(url, data=self.data)
        self.data.update({"id": response.data["id"]})
        assert response.status_code == status.HTTP_200_OK
        assert response.data == self.data

    @pytest.mark.run(order=4)
    def test_partial_update_user_details(self):
        """
            Does a partial update of the user
        """
        self.set_api_auth_header()
        user = User.objects.first()
        url = self.user_detail + str(user.pk) + "/"

        data = self.data
        data["username"] = "test_user"
        data["email"] = "test2@test.com"
        response = self.client.patch(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "test_user"
        assert response.data["email"] == "test2@test.com"

    @pytest.mark.run(order=5)
    def test_delete_user(self):
        """
            Deletes the user
        """
        self.set_api_auth_header()
        user = User.objects.first()
        url = self.user_detail + str(user.pk) + "/"

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
