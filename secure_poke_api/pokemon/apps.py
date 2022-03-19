from django.apps import AppConfig


class PokemonConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "secure_poke_api.pokemon"
    label = "pokemon"
