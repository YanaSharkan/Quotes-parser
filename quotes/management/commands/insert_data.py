from django.core.management.base import BaseCommand

from faker import Faker

from ...models import Author, Book, Quote


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('entities_count', type=int, choices=range(1, 1001))

    def handle(self, *args, **options):
        fake = Faker()
        entities_count = options['entities_count']
        for _ in range(entities_count):
            author_record = Author.objects.create(full_name=fake.name(),
                                                  about=fake.sentence(),
                                                  born=fake.date(),
                                                  location=fake.city())
            books_params = [{'name': fake.company(),
                             'author': author_record,
                             'pages': fake.random.randint(100, 1000)} for _ in range(entities_count)]
            for book_param in books_params:
                Book.objects.create(**book_param)

            quotes_params = [{'body': fake.sentence(3),
                             'author': author_record} for _ in range(entities_count)]
            for quote_param in quotes_params:
                Quote.objects.create(**quote_param)
