from django.contrib import admin

from .models import PokemonType


@admin.register(PokemonType)
class PokemonTypeAdmin(admin.ModelAdmin):

    list_display = ("slug",)
    list_display_links = ("slug",)
    search_fields = ("slug",)
    ordering = ("slug",)
