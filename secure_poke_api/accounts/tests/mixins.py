from secure_poke_api.accounts.models import User


class UserMixin:
    def any_user(self, email="pokemon@pokedex.com", password="1234", pokemon_types=None, **kwargs):

        extra_fields = {
            "is_staff": kwargs.setdefault("is_staff", True),
        }

        user = User.objects.create_user(email, **extra_fields)
        user.set_password(password)

        if pokemon_types:
            user.pokemon_types.set(pokemon_types)

        user.save()

        return user
