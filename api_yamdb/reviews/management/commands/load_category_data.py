from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = "Loads data from category.csv"

    def handle(self, *args, **options):

        with open('./static/data/category.csv', encoding='utf-8') as f:
            for row in DictReader(f):
                category = Category(
                    name=row['name'],
                    slug=row['slug']
                )
                category.save()
