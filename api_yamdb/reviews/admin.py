from django.contrib import admin


from .models import Titles, Category, Ganre, GanreTitles


admin.site.register(Titles)
admin.site.register(Category)
admin.site.register(Ganre)
admin.site.register(GanreTitles)
