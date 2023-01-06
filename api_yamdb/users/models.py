from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    ADMIN = ('admin', 'Администратор')
    MODERATOR = ('moderator', 'Модератор')
    USER = ('user', 'Пользователь')


class User(AbstractUser):
    bio = models.TextField(
        'О себе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
