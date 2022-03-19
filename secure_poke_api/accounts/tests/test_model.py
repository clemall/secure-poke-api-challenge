from django.test import TestCase

from ..models import User
from .mixins import UserMixin


class UserModelTestCase(UserMixin, TestCase):
    def test_user_model(self):
        """
        Given a user
        When I create it
        Then it is present in DB and the data is correct
        """
        user_created = self.any_user()

        users = User.objects.filter(email=user_created.email)
        self.assertEqual(users.count(), 1)

        user = users.first()
        self.assertEqual(str(user), user_created.email)
