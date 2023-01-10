from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Run all commands to load data from csv."

    def handle(self, *args, **options):
        commands = [
            'load_users_data',
            'load_category_data',
            'load_genre_data',
            'load_title_data',
            'load_genre_title_data',
            'load_review_data',
            'load_comments_data'
        ]

        for command in commands:
            call_command(command)
            self.stdout.write(
                self.style.SUCCESS(f'Command {command} executed successfully.')
            )
