from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from secure_poke_api.accounts.serializers import (
    AccountSerializer,
    SignupSerializer,
)

__all__ = ["SignupView", "MeView"]


class SignupView(APIView):
    """
    Create account for a new user and return the auth token in the response body
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        payload = user.get_auth_token()
        return Response(payload, status=status.HTTP_201_CREATED)


class MeView(APIView):
    """
    return user information
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
