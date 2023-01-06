from django.contrib import admin


from .models import Title, Category, Genre, GenreTitle, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройки отображения данных таблицы TITLES."""
    list_display = ('pk', 'name', 'year', 'description', 'category')


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Review)
admin.site.register(Comment)
