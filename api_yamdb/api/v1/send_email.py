from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_code(user, confirmation_code):
    """
    Функция отправляет код подтверждения на электронную почту пользователя.
    """
    subject = "You're signed up on YaMDB!"
    message = """
        Hello, {0}!
        Your confirmation code to receive a token is: {1}
        Note: it will expire in 1 day.
    """.format(user.username, confirmation_code)
    from_email = settings.DEFAULT_FROM_EMAIL
    recepient_list = [user.email]

    send_mail(subject, message, from_email, recepient_list)
