from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from secure_poke_api.accounts.serializers import (
    AccountSerializer,
    SignupSerializer,
)
from secure_poke_api.pokemon.models import PokemonType

__all__ = ["SignupView", "MeView", "AddToGroupView", "RemoveFromGroupView"]


class SignupView(APIView):
    """
    Create account for a new user and return the auth token in the response body
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        payload = user.get_auth_token()
        return Response(payload, status=status.HTTP_201_CREATED)


class MeView(APIView):
    """
    return user information
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToGroupView(APIView):
    """
    Add current user to the given group (pokémon type)
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pokemon_type):
        p_type = get_object_or_404(PokemonType, slug=pokemon_type)
        request.user.pokemon_types.add(p_type)
        serializer = AccountSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveFromGroupView(APIView):
    """
    Remove current user from the given group (pokémon type)
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pokemon_type):
        p_type = get_object_or_404(PokemonType, slug=pokemon_type)
        request.user.pokemon_types.remove(p_type)
        serializer = AccountSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
