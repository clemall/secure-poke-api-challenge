from secure_poke_api.pokemon.models import PokemonType


class PokemonTypeMixin:
    def any_pokemon_type(self, slug="fire"):
        pokemon_type, created = PokemonType.objects.get_or_create(slug=slug)
        return pokemon_type
