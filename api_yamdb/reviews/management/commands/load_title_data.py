from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Title


class Command(BaseCommand):
    help = "Loads data from titles.csv"

    def handle(self, *args, **options):

        with open('./static/data/titles.csv', encoding='utf-8') as f:
            for row in DictReader(f):
                title = Title(
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )
                title.save()
