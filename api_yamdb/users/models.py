from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = (
    ('ADM', 'admin'),
    ('MOD', 'moderator'),
    ('USR', 'user'),
)


class User(AbstractUser):
    bio = models.TextField(
        'О себе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=3,
        choices=USER_ROLES,
        default='USR'
    )
