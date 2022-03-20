import json

import requests
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

PokemonType = apps.get_model("pokemon", "PokemonType")


class Command(BaseCommand):
    help = "Populate the table PokemonType with https://pokeapi.co/ pokémon types"

    def handle(self, *args, **options):
        url = f"{settings.POKEAPI_BASE_URL}/type/"
        response = requests.get(url)

        pokeapi_types = []
        try:
            pokeapi_types = response.json()["results"]
        except json.JSONDecodeError:
            raise "Error while importing pokémon types from pokeapi"

        pokemon_type_to_create = []
        for pokeapi_type in pokeapi_types:
            slug = pokeapi_type["name"]
            if not PokemonType.objects.filter(slug=slug).exists():
                pokemon_type_to_create.append(PokemonType(slug=slug))

        PokemonType.objects.bulk_create(pokemon_type_to_create)
