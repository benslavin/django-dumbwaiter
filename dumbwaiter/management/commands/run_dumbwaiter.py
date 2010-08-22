from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from dumbwaiter.app import Dumbwaiter
        d = Dumbwaiter()
        d.run()