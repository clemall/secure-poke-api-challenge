from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from secure_poke_api.accounts.views import (
    AddToGroupView,
    MeView,
    RemoveFromGroupView,
    SignupView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="account_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="account_token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="account_token_verify"),
    path("signup/", SignupView.as_view(), name="account_signup"),
    path("me/", MeView.as_view(), name="account_me"),
    path("group/<str:pokemon_type>/add/", AddToGroupView.as_view(), name="account_add_to_group"),
    path("group/<str:pokemon_type>/remove/", RemoveFromGroupView.as_view(), name="account_remove_from_group"),
]
