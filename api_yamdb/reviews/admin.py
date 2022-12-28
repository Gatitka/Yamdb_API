from django.contrib import admin


from .models import Titles, Category, Genre, GenreTitles


admin.site.register(Titles)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitles)
