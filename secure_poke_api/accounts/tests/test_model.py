from django.test import TestCase

from ...pokemon.tests.mixins import PokemonTypeMixin
from ..models import User
from .mixins import UserMixin


class UserModelTestCase(UserMixin, PokemonTypeMixin, TestCase):
    def test_user_model(self):
        """
        Given a user with a pokémon type
        When I create it
        Then it is present in DB and the data is correct
        """
        pokemon_type = self.any_pokemon_type()
        user_created = self.any_user(pokemon_types=[pokemon_type])

        users = User.objects.filter(email=user_created.email)
        self.assertEqual(users.count(), 1)

        user = users.first()
        self.assertEqual(str(user), user_created.email)
        self.assertIn(pokemon_type.slug, user.pokemon_access_types)
