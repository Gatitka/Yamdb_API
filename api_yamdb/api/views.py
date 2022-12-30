from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title
from rest_framework.pagination import PageNumberPagination
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          WriteTitleSerializer)
from .filters import TitleFilter


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
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
