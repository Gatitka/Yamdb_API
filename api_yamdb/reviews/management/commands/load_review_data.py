from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Review


class Command(BaseCommand):
    help = "Loads data from review.csv"

    def handle(self, *args, **options):

        with open('./static/data/review.csv', encoding='utf-8') as f:
            for row in DictReader(f):
                review=Review(
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                review.save()
