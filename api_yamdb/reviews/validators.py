from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """ Валидация года создания произведения."""
    year = value
    if year:
        if year > timezone.now().year:
            raise ValidationError(
                'Дата публикации не может быть в будущем'
            )
        if year < 1895:
            raise ValidationError(
                'Дата публикации не может быть '
                'раньше появления кинематографа'
            )
        return value
    raise ValidationError(
        'Необходимо указать год создания произведения'
    )


def validate_score(value):
    """ Валидация оценки произведения в отзыве."""
    score = value
    if not (0 < score <= 10):
        raise ValidationError('Оцените от 1 до 10.')
    return value
