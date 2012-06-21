from django.core.management.base import BaseCommand

from folders.utils import sync_music


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_music()

# eof
