import json

import requests
from django.conf import settings
from rest_framework.exceptions import APIException


class PokeAPIError(APIException):
    def __init__(self, error_message):
        self.error_message = error_message


class PokeApi(object):
    """
    wrapper to call PokeAPI
    """

    @staticmethod
    def _replace_url(content):
        """
        Replace PokeApi pokemon/ url with project url
        """

        # Convert json to string to use the method replace
        content = json.dumps(content)
        content = content.replace(f"{settings.POKEAPI_BASE_URL}/pokemon/", f"{settings.BASE_URL_PROJECT}/api/pokemon/")
        # convert the content back to json
        content = json.loads(content)
        return content

    @classmethod
    def detail(cls, pokemon_id=None, pokemon_name=None):
        """
        return the response of PokeApi pokémon api with the given pokémon name/id
        """
        if pokemon_id is None and pokemon_name is None:
            raise PokeAPIError("Pokemon id or pokemon name must be provided")

        url = f"{settings.POKEAPI_BASE_URL}/pokemon/{pokemon_id or pokemon_name}"
        response = requests.get(url)

        try:
            response_data = cls._replace_url(response.json())
        except json.JSONDecodeError:
            raise PokeAPIError(f"{response.text} - {response.status_code}")

        return response_data

    @classmethod
    def _remove_duplicates(cls, data):
        """
        Remove duplicates in a list of pokémon
        """
        done = set()
        pokemons = []
        for pokemon in data:
            if pokemon["name"] not in done:
                done.add(pokemon["name"])
                pokemons.append(pokemon)
        return pokemons

    @classmethod
    def collection(cls, pokemon_types=None):
        if pokemon_types is None:
            raise PokeAPIError("Pokemon type must be provided")

        if len(pokemon_types) == 0:
            return []

        data = []
        session = requests.Session()
        for pokemon_type in pokemon_types:
            url = f"{settings.POKEAPI_BASE_URL}/type/{pokemon_type}?limit={settings.POKEAPI_LIMIT}"
            response = session.get(url)

            try:
                # we care only for the list of Pokémon that pokeapi return
                response_data = response.json()["pokemon"]
                data.extend(cls._replace_url(response_data))
            except json.JSONDecodeError:
                raise PokeAPIError(f"{response.text} - {response.status_code}")

        # we care only for the pokémon section of each item
        data = [item["pokemon"] for item in data]

        # When retrieving the lists of pokémon based on their types, we might have pokémon with multiples types.
        # Therefore, we need to remove the potential duplicates
        pokemons = cls._remove_duplicates(data)
        return pokemons
