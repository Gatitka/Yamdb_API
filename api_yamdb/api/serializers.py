from rest_framework import serializers
from reviews.models import Title, Genre, Category, GenreTitle, Review
import datetime
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True,)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title
# добавить поле рейтинг


class WriteTitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title

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


class ReviewSerializer(serializers.ModelSerializer):

    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
