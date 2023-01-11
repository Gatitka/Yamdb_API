import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели User.
    Все поля, кроме bio обязательны.
    Валидация:
    1) проверка, что переданный username не 'me';
    2) проверка уникальности полей email и username по БД.
    """

    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        model = User

    def validate_username(self, value):
        print("Валидация username == 'me'")
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Использовать 'me' в качестве username запрещено.")
        return value


class SignUpSerializer(UserSerializer):
    """
    Сериализатор для регистрации и получения кода потдверждения.
    Поля email и username обязательны.
    Валидация:
    - Если пользователь уже существует, данные считаются валидными;
    - Если в БД есть пользователи с переданными email или username,
    вызывается ошибка.
    """
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', max_length=150)

    class Meta:
        fields = ['email', 'username']
        model = User

    def validate(self, data):
        username = data['username']
        email = data['email']
        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует.")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует.")
        return data


class UserProfileSerializer(UserSerializer):
    """
    Сериализатор для получения и изменения данных
    собственной учётной записи.
    Пользователь может узнать свою роль в системе, но не может её изменять.
    """

    class Meta(UserSerializer.Meta):
        read_only_fields = ['role']


class MyTokenObtainSerializer(TokenObtainSerializer):
    """
    Сериализатор для получения JWT.
    Поля username и confirmation_code обязательны.
    Валидация:
    1) username должен соответсвовать шаблону: буквы, цифры и знаки @./+/-/_;
    2) проверка существования пользователя с полученным username;
    3) проверка переданного кода подтверждения для этого пользователя.
    """
    token_class = AccessToken
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', max_length=150)
    confirmation_code = serializers.CharField()

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    def validate(self, data):
        try:
            self.user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise NotFound("Пользователя с таким username не существует.")

        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(
            user=self.user,
            token=confirmation_code
        ):
            raise serializers.ValidationError(
                "Недействительный код подтверждения.")

        data = {"token": str(self.get_token(self.user))}

        return data


class GenreSerializer(serializers.ModelSerializer):
    """ Сериалайзер жанра."""
    class Meta:
        fields = ['name', 'slug']
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """ Сериалайзер категории."""
    class Meta:
        fields = ['name', 'slug']
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """ Сериалайзер произведения для чтения, вкл создание поля рейтинга."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        if Review.objects.filter(title=obj.id).exists():
            avg_score = Review.objects.filter(
                title=obj.id
            ).aggregate(Avg('score'))['score__avg']
            return round(avg_score)
        return None


class WriteTitleSerializer(TitleSerializer):
    """ Сериалайзер для записи произведения. Наследуется от TitleSerializer
    для десериализации на чтение(вкл поле рейтинга).
    Genre, category пишутся по slug.
    Валидация даты произведения."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    def validate(self, attrs):
        year = attrs.get('year')
        if year:
            if year > datetime.datetime.now().year:
                raise serializers.ValidationError(
                    'Дата публикации не может быть в будущем')
            if year < 1895:
                raise serializers.ValidationError(
                    'Дата публикации не может быть '
                    'раньше появления кинематографа')
        return attrs

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError(
                'Поле категории не может быть пустым')
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            genre = get_object_or_404(Genre, slug=genre)
            GenreTitle.objects.create(
                genre=genre, title=title)
        return title

    def to_representation(self, value):
        serializer = TitleSerializer(value)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор для чтения и редакции отзывов.
    (НЕТ Валидации: 1 отзыв на 1 произведение)
    Валидация оценки произведению 0-10."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review

    def validate_score(self, value):
        if not (0 < value <= 10):
            raise serializers.ValidationError('Оцените от 1 до 10.')
        return value


class WriteReviewSerializer(ReviewSerializer):
    """ Сериализатор для сохдания отзывов.
    Валидация 1 отзыв на 1 произведение.
    Валидация оценки произведению 0-10"""

    def validate(self, data):
        request = self.root.context['request']
        kwargs = request.parser_context['kwargs']
        title_id = kwargs['title_id']

        if Review.objects.filter(author=request.user, title=title_id):
            raise serializers.ValidationError(
                'Пользователь может добавить лишь один отзыв на произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализаторя для комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
