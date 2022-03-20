from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from secure_poke_api.pokemon.services.pokeapi import PokeApi

__all__ = ["PokemonDetailView", "PokemonCollectionView"]


class PokemonDetailView(APIView):
    """
    Returns PokeApi response with Pokémon details.
    User must share at least one type with the requested pokémon to be able to see the detail of that pokémon.
    Example: user with type [fire, steel] can see the detail of charizard [fire, flying]
    since they share the type [fire], even the user is missing the type [flying].
    """

    permission_classes = [IsAuthenticated]

    def retrieve_types(self, pokemon_details):
        types = []
        for data in pokemon_details["types"]:
            types.append(data["type"]["name"])
        return types

    def get(self, request, pokemon_param):
        pokemon_details = PokeApi.detail(pokemon_param)

        types = self.retrieve_types(pokemon_details)
        user_pokemon_types = request.user.pokemon_access_types

        if any(user_pokemon_type in user_pokemon_types for user_pokemon_type in types):
            return Response(pokemon_details, status=status.HTTP_200_OK)

        else:
            missing_types = list(set(types) - set(user_pokemon_types))
            raise ValidationError(f"You don't have access to Pokémon types: {missing_types}")


class PokemonCollectionView(APIView):
    """
    Returns PokeApi with Pokémon collection.
    The collection will contain all Pokémon that have at least one matching type with the
    user's type.
    Example: user with type [fire, steel] will be able to see charizard [fire, flying]
    since both share the [fire] type.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_pokemon_types = request.user.pokemon_access_types
        pokemon_collection = PokeApi.collection(user_pokemon_types)

        return Response(pokemon_collection, status=status.HTTP_200_OK)
