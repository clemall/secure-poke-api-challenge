import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ...pokemon.tests.mixins import PokemonTypeMixin
from .mixins import UserMixin

User = get_user_model()


class AccountViewTestCase(UserMixin, PokemonTypeMixin, TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.client = APIClient()

        self.LOGIN = "accounts:account_login"
        self.SIGNUP = "accounts:account_signup"
        self.ME = "accounts:account_me"
        self.ADD_TO_GROUP = "accounts:account_add_to_group"
        self.REMOVE_FROM_GROUP = "accounts:account_remove_from_group"

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
        Given a user with a pokémon type
        When I call me
        Then response is 200 and I get the user information
        """
        pokemon_type = self.any_pokemon_type()
        user = self.any_user(pokemon_types=[pokemon_type])
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        response = self.client.get(reverse(self.ME), format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            json.loads(response.content),
            {
                "email": user.email,
                "group": [{"slug": pokemon_type.slug}],
            },
        )

    def test_add_to_group(self):
        """
        Given a user without a pokémon type
        When I call add_to_group
        Then response is 200 and user is in the group
        """
        pokemon_type = self.any_pokemon_type()
        user = self.any_user()
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        url = reverse(self.ADD_TO_GROUP, kwargs={"pokemon_type": pokemon_type.slug})

        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "email": user.email,
                "group": [{"slug": pokemon_type.slug}],
            },
        )

    def test_remove_from_group(self):
        """
        Given a user with a pokémon type
        When I call remove_from_group
        Then response is 200 and user is removed from the group
        """
        pokemon_type = self.any_pokemon_type()
        user = self.any_user(pokemon_types=[pokemon_type])
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        url = reverse(self.REMOVE_FROM_GROUP, kwargs={"pokemon_type": pokemon_type.slug})

        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "email": user.email,
                "group": [],
            },
        )
