from rest_framework import status
from rest_framework.test import APITestCase


# test the user registration endpoint
class TestAuthAPI(APITestCase):
    def setUp(self):
        # create a new user making a post request to user register endpoint
        self.data = {
            "email": "test@test.com",
            "password": "secret",
            "password2": "secret",
        }
        self.user = self.client.post("/api/auth/register/", data=self.data)

    def test_user_login(self):
        """
            test user login
        """
        response = self.client.post("/api/auth/login/", data=self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_user_registration(self):
        """
            test user registration
        """
        data = {
            "email": "test2@test.com",
            "password": "secret",
            "password2": "secret",
        }
        response = self.client.post("/api/auth/register/", data)
        response_data = {"response": "success", "message": "user created succesfully"}
        assert response.status_code == status.HTTP_200_OK
        assert response.data == response_data
