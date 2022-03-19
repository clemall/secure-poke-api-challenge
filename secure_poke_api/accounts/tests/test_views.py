import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .mixins import UserMixin

User = get_user_model()


class AccountViewTestCase(UserMixin, TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.client = APIClient()

        self.LOGIN = "accounts:account_login"
        self.SIGNUP = "accounts:account_signup"
        self.ME = "accounts:account_me"

    def test_signin(self):
        """
        Given a user
        When I call signin
        Then response is 200
        """
        user_data = {"email": "pokemon@pokedex.com", "password": "pokemon1"}
        self.any_user(**user_data)

        response = self.client.post(reverse(self.LOGIN), data=user_data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_signin_wrong_email(self):
        """
        Given a user
        When I call signin with wrong email
        Then response is 401
        """
        user_data = {"email": "pokemon@pokedex.com", "password": "pokemon1"}
        self.any_user(**user_data)

        response = self.client.post(
            reverse(self.LOGIN),
            data={"email": "foo@bar.fake.com", "password": "pokemon1"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_signup(self):
        """
        Given a user information
        When I call signup
        Then response is 200 and user object is correct
        """
        user_data = {"email": "pokemon@pokedex.com", "password": "pokemon1"}
        response = self.client.post(reverse(self.SIGNUP), data=user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, user_data["email"])

    def test_me(self):
        """
        Given a user
        When I call me
        Then response is 200 and I get the user information
        """
        user = self.any_user()
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        response = self.client.get(reverse(self.ME), format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            json.loads(response.content),
            {
                "email": user.email,
            },
        )
