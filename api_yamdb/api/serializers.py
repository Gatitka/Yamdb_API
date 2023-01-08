import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Genre, GenreTitle, Review, Title, Comment


class UserSerializer(serializers.ModelSerializer):

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
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Использовать 'me' в качестве username запрещено.")
        return value


class SignUpSerializer(UserSerializer):

    class Meta:
        fields = ['email', 'username']
        model = User


class UserProfileSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ['role']


class MyTokenObtainSerializer(TokenObtainSerializer):
    token_class = AccessToken
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', max_length=150)
    confirmation_code = serializers.CharField()

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

        self.fields['username'] = serializers.CharField(max_length=150)
        self.fields['confirmation_code'] = serializers.CharField()

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
        return 0


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
    """ Сериализатор для отзывов. Валидация: 1 отзыв на 1 произведение.
    Валидация оценки произведению 0-10"""
    # author = serializers.SlugRelatedField(
    #     default=serializers.CurrentUserDefault(),
    #     slug_field='username',
    #     read_only=True
    # )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review

    def validate(self, data):
        request = self.root.context['request']
        kwargs = request.parser_context['kwargs']
        title_id = kwargs['title_id']

        if Review.objects.filter(author=data['author'], title=title_id):
            raise serializers.ValidationError(
                f'Пользователь может добавить лишь один отзыв на произведение.'
            )
        return data

    def validate_score(self, value):
        if not (0 < value <= 10):
            raise serializers.ValidationError('Оцените от 1 до 10.')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализаторя для комментариев к отзывам."""
    # author = serializers.SlugRelatedField(
    #     default=serializers.CurrentUserDefault(),
    #     slug_field='username',
    #     read_only=True
    # )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
