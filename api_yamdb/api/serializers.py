import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Genre, GenreTitle, Review, Title, Comment


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
                    'Дата публикации не может быть раньше появления кино')
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
