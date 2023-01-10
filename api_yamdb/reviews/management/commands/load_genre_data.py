from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Genre


class Command(BaseCommand):
    help = "Loads data from genre.csv"

    def handle(self, *args, **options):

        with open('./static/data/genre.csv', encoding='utf-8') as f:
            for row in DictReader(f):
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                genre.save()
