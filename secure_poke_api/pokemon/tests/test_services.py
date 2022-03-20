from django.test import TestCase

from ..services.pokeapi import PokeApi, PokeAPIError
from .mixins import PokemonTypeMixin


class ServicesTestCase(PokemonTypeMixin, TestCase):
    """
    These tests are flaky as they depend on an external API
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.POKEMON_NAME = "charizard"
        self.POKEMON_ID = 6
        self.POKEMON_TYPE = "fire"

    def test_pokeapi_detail(self):
        """
        Given a pokémon name
        When I call pokeapi service detail
        Then I get the pokémon detail
        """
        result = PokeApi.detail(pokemon_name=self.POKEMON_NAME)
        self.assertGreater(len(result), 0)
        self.assertEqual(result["types"][0].keys(), {"slot", "type"})
        self.assertEqual(result["types"][0]["type"].keys(), {"name", "url"})

    def test_pokeapi_detail__id(self):
        """
        Given a pokémon id
        When I call pokeapi service detail
        Then I get the pokémon detail
        """
        result = PokeApi.detail(pokemon_name=self.POKEMON_ID)
        self.assertGreater(len(result), 0)
        self.assertEqual(result["types"][0].keys(), {"slot", "type"})
        self.assertEqual(result["types"][0]["type"].keys(), {"name", "url"})

    def test_pokeapi_detail__no_params(self):
        """
        Given no  parameters
        When I call pokeapi service detail
        Then an error is raised
        """
        with self.assertRaises(PokeAPIError):
            PokeApi.detail()

    def test_pokeapi_detail__wrong_pokemon(self):
        """
        Given a wrong pokémon name
        When I call pokeapi service detail
        Then an error is raised
        """
        with self.assertRaises(PokeAPIError):
            PokeApi.detail(pokemon_name="batman")

    def test_pokeapi_collection(self):
        """
        Given a pokémon type
        When I call pokeapi service collection
        Then I get the pokémon collection
        """

        result = PokeApi.collection(pokemon_types=[self.POKEMON_TYPE])
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0].keys(), {"name", "url"})

    def test_pokeapi_collection__no_params(self):
        """
        Given no pokémon types
        When I call pokeapi service collection
        Then an error is raised
        """
        with self.assertRaises(PokeAPIError):
            PokeApi.collection()

    def test_pokeapi_collection__empty_params(self):
        """
        Given a pokémon type
        When I call pokeapi service collection
        Then I get an empty list
        """

        result = PokeApi.collection(pokemon_types=[])
        self.assertEqual(len(result), 0)

    def test_pokeapi_collection__wrong_param(self):
        """
        Given a pokémon type that doesn't exist
        When I call pokeapi service collection
        Then an error is raised
        """
        with self.assertRaises(PokeAPIError):
            PokeApi.collection(pokemon_types=["batman"])

    def test_pokeapi_collection_remove_duplicates(self):
        """
        Given a list of pokémon with duplicates
        When I call _remove_duplicates
        Then I get a list with no duplicates
        """
        data = [
            {"name": "charmander", "url": "http://localhost:8000/api/pokemon/4/"},
            {"name": "charmeleon", "url": "http://localhost:8000/api/pokemon/5/"},
            {"name": "charmander", "url": "http://localhost:8000/api/pokemon/4/"},
        ]
        result = PokeApi._remove_duplicates(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            result,
            [
                {"name": "charmander", "url": "http://localhost:8000/api/pokemon/4/"},
                {"name": "charmeleon", "url": "http://localhost:8000/api/pokemon/5/"},
            ],
        )
