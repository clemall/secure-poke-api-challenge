from django.test import TestCase

from ...pokemon.tests.mixins import PokemonTypeMixin
from ..serializers import AccountSerializer
from .mixins import UserMixin


class UserSerialiserTestCase(UserMixin, PokemonTypeMixin, TestCase):
    def test_user_account_serializer(self):
        """
        Given a user with a pokémon type
        When I serialize
        Then data is valid
        """
        pokemon_type = self.any_pokemon_type()
        user = self.any_user(pokemon_types=[pokemon_type])

        serializer = AccountSerializer(instance=user)
        data = serializer.data
        self.assertEqual(data["email"], user.email)
        self.assertIn(pokemon_type.slug, user.pokemon_access_types)

    def test_user_account_serializer__many_types(self):
        """
        Given a user with multiples pokémon type
        When I serialize
        Then data is valid
        """
        pokemon_type_1 = self.any_pokemon_type("electric")
        pokemon_type_2 = self.any_pokemon_type("steel")
        user = self.any_user(pokemon_types=[pokemon_type_1, pokemon_type_2])

        serializer = AccountSerializer(instance=user)
        data = serializer.data

        self.assertEqual(data["email"], user.email)
        self.assertIn(pokemon_type_1.slug, user.pokemon_access_types)
        self.assertIn(pokemon_type_2.slug, user.pokemon_access_types)
