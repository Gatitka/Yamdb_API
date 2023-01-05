from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryCreateDestroyListViewSet,
                       GenreCreateDestroyListViewSet, SignUpView,
                       TitleViewSet, TokenObtainView)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    'categories',
    CategoryCreateDestroyListViewSet,
    basename='categories'
)
v1_router.register('genres', GenreCreateDestroyListViewSet, basename='genres')

# v1_router.register(r'v1/posts/(?P<post_id>\d+)/comments',
#                    CommentViewSet,
#                    basename='comments')
# v1_router.register('v1/follow', FollowCreateListViewSet, basename='groups')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', SignUpView.as_view()),
    path('auth/token/', TokenObtainView.as_view())
]
