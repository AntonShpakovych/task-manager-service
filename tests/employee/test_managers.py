from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserManagerTest(TestCase):
    def test_create_customer_user(self):
        position = "Admin"

        admin_data = {
            "username": "First!admin",
            "password": "Crasw1231!",
            "email": "someemail@gmail.com",
        }

        self.assertEqual(
            get_user_model().objects.create_superuser(
                **admin_data
            ).position.name,
            position,
        )
