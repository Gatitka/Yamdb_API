from api.views import TitleViewSet, CategoryCreateDestroyListViewSet, GenreCreateDestroyListViewSet, ReviewViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryCreateDestroyListViewSet, basename='categories')
v1_router.register('genres', GenreCreateDestroyListViewSet, basename='genres')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')

urlpatterns = [
    path('', include(v1_router.urls)),
]
