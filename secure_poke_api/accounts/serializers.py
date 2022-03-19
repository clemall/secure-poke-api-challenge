from rest_framework import serializers

from secure_poke_api.accounts.models import User
from secure_poke_api.pokemon.models import PokemonType

__all__ = ["SignupSerializer", "AccountSerializer"]


class PokemonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonType
        fields = ["slug"]


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    group = PokemonTypeSerializer(many=True, read_only=True, source="pokemon_types")

    class Meta:
        model = User
        fields = ("email", "group")


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
