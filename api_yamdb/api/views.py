from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorAdminModerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MyTokenObtainSerializer,
                          ReviewSerializer, SignUpSerializer, TitleSerializer,
                          UserProfileSerializer, UserSerializer,
                          WriteReviewSerializer, WriteTitleSerializer)

User = get_user_model()


def send_confirmation_code(user, confirmation_code):
    subject = "You're signed up on YaMDB!"
    message = (f'Hello, {user.username}!\n'
               'Your confirmation code to receive a token is: '
               f'{confirmation_code}\n'
               'Note: code will expire in 1 day.')
    from_email = 'hello@yamdb.ru'
    recepient_list = [user.email, ]

    send_mail(subject, message, from_email, recepient_list)


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        user = None
        if not serializer.is_valid():
            try:
                user = User.objects.get(
                    username__iexact=serializer.initial_data.get('username'),
                    email__iexact=serializer.initial_data.get('email')
                )
            except User.DoesNotExist:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not user:
            user = serializer.save()
        confirmation_code = default_token_generator.make_token(user=user)
        send_confirmation_code(user, confirmation_code)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer
    permission_classes = [AllowAny]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

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


class TitleViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Title, сериализатор подбирается по типу запроса."""
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
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
    """ Вьюсет модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Review. Сериализатор подбирается по типу запроса для
    валидации 1автор-1произведение-1отзыв при создании. В других экшенах
    этой валидации нет."""
    permission_classes = [IsAuthorAdminModerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return WriteReviewSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ Вьюсет модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly]

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
        serializer.save(review=review, author=self.request.user)
