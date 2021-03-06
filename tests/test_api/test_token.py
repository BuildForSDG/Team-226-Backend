from rest_framework import status
from rest_framework.test import APITestCase


# test the user registration endpoint
class TestTokenAPI(APITestCase):

    data = {
        "email": "test@test.com",
        "password": "secret",
        "password2": "secret",
        "first_name": "test",
        "last_name": "user",
    }

    def setUp(self):
        # create a new user making a post request to register endpoint
        data = self.data
        self.client.post("/api/auth/register/", data=data)

        response = self.client.post("/api/auth/token/", data=data)
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]

    # retrieve token
    def test_get_tokens(self):
        """ get both the access and refresh tokens """
        response = self.client.post("/api/auth/token/", data=self.data)
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_refresh_token(self):
        """ uses the refresh token to get a new access token """
        data = {"refresh": self.refresh_token}
        response = self.client.post("/api/auth/token/refresh/", data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_verify_token(self):
        """ verifies the access token if it's still valid """
        data = {"token": self.access_token}
        response = self.client.post("/api/auth/token/verify/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {}
