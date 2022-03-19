from django.test import TestCase

from ..models import PokemonType
from .mixins import PokemonTypeMixin


class PokemonTypeModelTestCase(PokemonTypeMixin, TestCase):
    def test_pokemon_type_model(self):
        """
        Given a pokémon type
        When I create it
        Then it is present in DB and the data is correct
        """
        pokemon_type = self.any_pokemon_type()

        pokemon_type_created = PokemonType.objects.filter(slug=pokemon_type.slug)

        self.assertEqual(pokemon_type_created.count(), 1)
        # test __str__
        self.assertEqual(str(pokemon_type_created.first()), pokemon_type.slug)
