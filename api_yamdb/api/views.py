from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title, Comment

from .filters import TitleFilter
from .serializers import (CategorySerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer,
                          WriteTitleSerializer, CommentSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Title, сериализатор подбирается по типу запроса."""
    queryset = Title.objects.all()
    # permission_classes = None
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return WriteTitleSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(TitleSerializer(serializer.instance), status=status.HTTP_201_CREATED)


class CategoryCreateDestroyListViewSet(mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.ListModelMixin,
                                       viewsets.GenericViewSet):
    """ Вьюсет модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    # permission_classes = None
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GenreCreateDestroyListViewSet(mixins.CreateModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    """ Вьюсет модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    # permission_classes = None

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Review."""
    serializer_class = ReviewSerializer
    # permission_classes = None

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Comment."""
    serializer_class = CommentSerializer
    # permission_classes = None

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return Comment.objects.filter(
            review__title=title.id,
            review=review.id
            ).all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(review=review)
