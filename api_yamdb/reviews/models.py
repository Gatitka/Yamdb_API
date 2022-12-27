from django.db import models


class Category(models.Model):
    """ Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории."""
    name = models.CharField(max_length=16)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ganre(models.Model):
    """ Жанры произведений. Одно произведение может быть привязано к
    нескольким жанрам."""
    name = models.CharField(max_length=16)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    """ Произведения, к которым пишут отзывы (определённый фильм, книга или
    песенка)."""
    name = models.CharField(max_length=16)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.CASCADE
        )
    ganre = models.ManyToManyField(Ganre, through='GanreTitles')
    # rating = models.IntegerField() подумать, возможно это поле сделать
    # лишь в сериализаторе - как часто выводится, чтобы не прописывать в
    # несокльких сериализаторах

    def __str__(self):
        return self.name


class GanreTitles(models.Model):
    """ Модель для сопоставления жанра и произведения."""
    ganre = models.ForeignKey(Ganre, on_delete=models.CASCADE)
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ganre} {self.titles}'
