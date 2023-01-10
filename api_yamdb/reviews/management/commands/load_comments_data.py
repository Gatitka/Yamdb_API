from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Comment


class Command(BaseCommand):
    help = "Loads data from comments.csv"

    def handle(self, *args, **options):

        with open('./static/data/comments.csv', encoding='utf-8') as f:
            for row in DictReader(f):
                comment = Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )
                comment.save()
