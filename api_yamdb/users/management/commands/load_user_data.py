from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Loads data from users.csv"

    def handle(self, *args, **options):

        with open('./static/data/users.csv', encoding='utf-8') as f:
            for row in DictReader(f):
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                user.save()
