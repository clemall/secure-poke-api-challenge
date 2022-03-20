from django.urls import path

from secure_poke_api.pokemon.views import (
    PokemonCollectionView,
    PokemonDetailView,
)

app_name = "pokemon"

urlpatterns = [
    path("pokemon/", PokemonCollectionView.as_view(), name="pokemon_collection"),
    path("pokemon/<pokemon_param>/", PokemonDetailView.as_view(), name="pokemon_detail"),
]
