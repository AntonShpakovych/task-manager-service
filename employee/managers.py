from django.contrib.auth.models import UserManager

import employee


class CustomUserManager(UserManager):
    def create_superuser(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # here I used that type of getting model to avoid circular import

        position, _ = employee.models.Position.objects.get_or_create(
            name="Admin"
        )
        extra_fields.setdefault("position", position)
        return self._create_user(username, email, password, **extra_fields)
