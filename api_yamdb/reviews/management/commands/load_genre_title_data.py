from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import GenreTitle


class Command(BaseCommand):
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):

        with open('./static/data/genre_title.csv', encoding='utf-8') as f:
            for row in DictReader(f):
                genretitle = GenreTitle(
                    id=row['id'],
                    genre_id=row['genre_id'],
                    title_id=row['title_id']
                )
                genretitle.save()
