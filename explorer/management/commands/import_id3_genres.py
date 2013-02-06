from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from folders.models import Genre


class Command(BaseCommand):
    help = 'Import ID3 genres as dumped to a file with the command: id3v2 -L'

    def handle(self, *args, **options):
        for filepath in args:
            listfile = open(filepath)
            for line in listfile.readlines():
                (id3_id, id3_name) = line.strip().split(': ')
                try:
                    genre = Genre(name=id3_name, id3_id=id3_id)
                    genre.save()
                    print '* imported genre: %s' % genre
                except IntegrityError:
                    pass

# eof
