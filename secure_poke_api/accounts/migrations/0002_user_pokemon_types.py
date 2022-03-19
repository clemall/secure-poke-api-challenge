from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="pokemon_types",
            field=models.ManyToManyField(blank=True, to="pokemon.pokemontype"),
        ),
    ]
