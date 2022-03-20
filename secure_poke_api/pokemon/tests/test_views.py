from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ...accounts.tests.mixins import UserMixin
from ...pokemon.tests.mixins import PokemonTypeMixin

User = get_user_model()


class PokemonViewTestCase(UserMixin, PokemonTypeMixin, TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.client = APIClient()

        self.COLLECTION = "pokemon:pokemon_collection"
        self.DETAIL = "pokemon:pokemon_detail"

        self.POKEMON_NAME = "charizard"
        self.POKEMON_ID = 6

    def test_collection(self):
        """
        Given a user with a pokémon type
        When I call pokémon collection
        Then response is 200
        """
        pokemon_type = self.any_pokemon_type()
        user = self.any_user(pokemon_types=[pokemon_type])
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        response = self.client.get(reverse(self.COLLECTION), format="json")
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertGreater(len(response_json), 0)
        self.assertEqual(response_json[0].keys(), {"name", "url"})

    def test_collection__no_types(self):
        """
        Given a user with no pokémon type
        When I call pokémon collection
        Then response is 200 with no data
        """
        user = self.any_user()
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        response = self.client.get(reverse(self.COLLECTION), format="json")
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json), 0)

    def test_detail(self):
        """
        Given a user with a pokémon type
        When I call pokémon detail with a pokémon sharing the same type as the user
        Then response is 200
        """
        pokemon_type_fire = self.any_pokemon_type("fire")
        pokemon_type_flying = self.any_pokemon_type("flying")
        user = self.any_user(pokemon_types=[pokemon_type_fire, pokemon_type_flying])
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        url = reverse(self.DETAIL, kwargs={"pokemon_param": self.POKEMON_NAME})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertGreater(len(response_json), 0)
        self.assertEqual(response_json["types"][0].keys(), {"slot", "type"})
        self.assertEqual(response_json["types"][0]["type"].keys(), {"name", "url"})

    def test_detail__half_type(self):
        """
        Given:
            a user with only [fire] as pokémon type
            a pokémon with [fire, flying] as pokémon type
        When I call pokémon detail
        Then response is 200
        """
        pokemon_type_fire = self.any_pokemon_type("fire")
        user = self.any_user(pokemon_types=[pokemon_type_fire])
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        url = reverse(self.DETAIL, kwargs={"pokemon_param": self.POKEMON_NAME})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertGreater(len(response_json), 0)
        self.assertEqual(response_json["types"][0].keys(), {"slot", "type"})
        self.assertEqual(response_json["types"][0]["type"].keys(), {"name", "url"})

    def test_detail__mismatch_type(self):
        """
        Given:
            a user with only [ice] as pokémon type
            a pokémon with [fire, flying] as pokémon type
        When I call pokémon detail
        Then response is 400
        """
        pokemon_type_fire = self.any_pokemon_type("ice")
        user = self.any_user(pokemon_types=[pokemon_type_fire])
        token = user.get_auth_token()

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])

        url = reverse(self.DETAIL, kwargs={"pokemon_param": self.POKEMON_NAME})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, text="You don't have access to Pokémon type", status_code=400)
