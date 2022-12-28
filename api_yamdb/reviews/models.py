from django.db import models


class Category(models.Model):
    """ Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Жанры произведений. Одно произведение может быть привязано к
    нескольким жанрам."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    """ Произведения, к которым пишут отзывы (определённый фильм, книга или
    песенка)."""
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL
        )
    genre = models.ManyToManyField(Genre, through='GenreTitles')
    # rating = models.IntegerField() подумать, возможно это поле сделать
    # лишь в сериализаторе - как часто выводится, чтобы не прописывать в
    # несокльких сериализаторах

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
    """ Модель для сопоставления жанра и произведения."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.titles}'
