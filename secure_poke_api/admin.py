from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from secure_poke_api.accounts.models import User

admin.site.register(User, UserAdmin)
