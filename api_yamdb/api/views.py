from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title, Review
from rest_framework.pagination import PageNumberPagination
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          WriteTitleSerializer, ReviewSerializer)
from .filters import TitleFilter
from django.shortcuts import get_object_or_404

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # permission_classes = None
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return WriteTitleSerializer


class CategoryCreateDestroyListViewSet(mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.ListModelMixin,
                                       viewsets.GenericViewSet):

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

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    # permission_classes = None

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (AuthorOrReadOnlyAnon,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(title=title)
