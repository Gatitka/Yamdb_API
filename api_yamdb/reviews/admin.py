from django.contrib import admin


from .models import Title, Category, Genre, GenreTitle, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройки отображения данных таблицы TITLES."""
    list_display = ('pk', 'name', 'year', 'description', 'category')


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review)
