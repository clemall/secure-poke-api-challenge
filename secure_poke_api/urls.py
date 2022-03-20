from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("secure_poke_api.accounts.urls")),
    path("api/", include("secure_poke_api.pokemon.urls")),
]
