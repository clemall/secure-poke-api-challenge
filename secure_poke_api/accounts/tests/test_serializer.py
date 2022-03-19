from django.test import TestCase

from ..serializers import AccountSerializer
from .mixins import UserMixin


class UserSerialiserTestCase(UserMixin, TestCase):
    def test_user_account_serializer(self):
        """
        Given a user
        When I serialize
        Then data is valid
        """
        user = self.any_user()

        serializer = AccountSerializer(instance=user)
        data = serializer.data
        self.assertEqual(data["email"], user.email)
