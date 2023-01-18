from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Genre, Review, Title

from ..viewsets import CreateDestroyListModelViewSet
from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorAdminModerOrReadOnly
)
from .send_email import send_confirmation_code
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    MyTokenObtainSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    UserProfileSerializer,
    UserSerializer,
    WriteTitleSerializer
)

User = get_user_model()


class SignUpView(views.APIView):
    """
    Вью-класс для самостоятельной регистрации нового пользователя
    и для получения кода подтверждения для пользователя,
    зарегистрированного админом.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
        confirmation_code = default_token_generator.make_token(user=user)
        send_confirmation_code(user, confirmation_code)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenObtainPairView):
    """
    Вьюсет для получения JWT.
    """
    serializer_class = MyTokenObtainSerializer
    permission_classes = [AllowAny]


class UsersViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели User. Метод PUT недоступен.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_instance(self):
        return self.request.user

    @action(
        detail=False,
        methods=['get', 'patch'],
        serializer_class=UserProfileSerializer,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def user_profile(self, request):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request)
        return self.partial_update(request)

    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Title, сериализатор подбирается по типу запроса."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return WriteTitleSerializer


class CategoryViewSet(CreateDestroyListModelViewSet):
    """ Вьюсет модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListModelViewSet):
    """ Вьюсет модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Review."""
    permission_classes = [IsAuthorAdminModerOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title_id=title_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(review=review, author=self.request.user)
