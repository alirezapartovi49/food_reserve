import json

from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse


class FullFlowAccountTest(TestCase):
    """test flow of account create, update, delete and get profile"""

    _user_creation_data = {
        "email": "test@gmail.com",
        "username": "test-username",
        "password": "Passwd123?",
        "password2": "Passwd123?",
    }

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=False)

    def test_auth_flow(self) -> None:
        self.create_user()
        self.login()

    def create_user(self):
        register_url = reverse("auth:register")
        self.user_data: dict = self._user_creation(register_url)
        self._bad_user_creation(register_url)

    def login(self):
        login_url = reverse("auth:login")
        data = {
            "email": self._user_creation_data["email"],
            "password": self._user_creation_data["password"],
        }
        response = self.client.post(login_url, data)
        self.assertContains(response, "token", status_code=200, html=False)
        self.user_data: dict = json.loads(response.content.decode())
        self.user_token = "Bearer " + self.user_data["token"]

    def _bad_user_creation(self, register_url) -> None:
        self._user_creation_data["password"] = "jcjdjcdjn"
        response = self.client.post(register_url, data=self._user_creation_data)
        self.assertEqual(response.status_code, 400)

        self._user_creation_data["password"] = "Passwd123?"
        response = self.client.post(register_url, data=self._user_creation_data)
        self.assertEqual(response.status_code, 400, msg=response.content.decode())

    def _user_creation(self, register_url) -> dict:
        response = self.client.post(register_url, data=self._user_creation_data)
        self.assertContains(
            response=response, text="token", status_code=201, html=False
        )

        decoded_content = response.content.decode()
        user_data = json.loads(decoded_content)

        self.assertIn("id", user_data)
        self.assertTrue(type(user_data["id"]) is int)

        return user_data
