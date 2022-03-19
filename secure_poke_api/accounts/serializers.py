from rest_framework import serializers

from secure_poke_api.accounts.models import User

__all__ = ["SignupSerializer", "AccountSerializer"]


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email",)


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
