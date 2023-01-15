from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles(models.TextChoices):
    ADMIN = ('admin', 'Администратор')
    MODERATOR = ('moderator', 'Модератор')
    USER = ('user', 'Пользователь')


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
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

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_moderator(self):
        return self.role == 'moderator'
