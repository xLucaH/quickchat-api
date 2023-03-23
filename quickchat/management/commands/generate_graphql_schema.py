from django.core.management.base import BaseCommand

from graphql.utils import schema_printer

from chat.schema import schema

class Command(BaseCommand):
    help = "Creates a .graphql file that represents the current schema of the api."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        my_schema_str = schema_printer.print_schema(schema)
        fp = open("static/schema.graphql", "w")
        fp.write(my_schema_str)
        fp.close()
