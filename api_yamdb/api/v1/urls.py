from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryCreateDestroyListViewSet,
    GenreCreateDestroyListViewSet,
    SignUpView,
    TitleViewSet,
    TokenObtainView,
    UsersViewSet,
    ReviewViewSet,
    CommentViewSet
)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('users', UsersViewSet)
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
v1_router.register(
    'categories',
    CategoryCreateDestroyListViewSet,
    basename='categories'
)
v1_router.register(
    'genres',
    GenreCreateDestroyListViewSet,
    basename='genres'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_create')
]
