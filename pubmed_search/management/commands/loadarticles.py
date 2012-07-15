from django.core.management.base import BaseCommand
from pubmed_search.utils import load_json_from_file

class Command(BaseCommand):
    args = '<filename filename ...>'
    help = """Parses the specified JSON files and loads the file contents into
    the database. Also calculates term frequency per document."""

    def handle(self, *args, **options):
        for filename in args:
            load_json_from_file(filename)
