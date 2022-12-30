from django.db import models


class Category(models.Model):
    """ Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Жанры произведений. Одно произведение может быть привязано к
    нескольким жанрам."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """ Произведения, к которым пишут отзывы (определённый фильм, книга или
    песенка)."""
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    # rating = models.IntegerField() подумать, возможно это поле сделать
    # лишь в сериализаторе - как часто выводится, чтобы не прописывать в
    # несокльких сериализаторах

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """ Модель для сопоставления жанра и произведения."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
