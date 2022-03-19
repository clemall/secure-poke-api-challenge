from django.db import models

__all__ = ["PokemonType"]


class PokemonType(models.Model):
    slug = models.SlugField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.slug
