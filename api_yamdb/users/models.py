from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLE = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


class User(AbstractUser):
    confirmation_code = models.IntegerField(default=0000)
    role = models.CharField(
        max_length=15,
        choices=USER_ROLE,
        default='user',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)

    @property
    def is_administrator(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
