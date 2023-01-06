import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, GenreTitle, Title

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True
    )
    username = serializers.CharField(
        max_length=150,
        required=True
    )

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
                "Использовать имя 'me' в качестве username запрещено.")
        return value


class SignUpSerializer(UserSerializer):

    class Meta:
        fields = ['email', 'username']
        model = User

    def create(self, validated_data):
        user, status = User.objects.get_or_create(**validated_data)
        return user


class MyTokenObtainSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

        self.fields['username'] = serializers.CharField(max_length=150)
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, data):
        try:
            self.user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователя с таким username не существует.")

        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(
            user=self.user,
            token=confirmation_code
        ):
            raise serializers.ValidationError(
                "Недействительный код подтверждения.")

        data = {"token": str(self.get_token(self.user))}

        return data
