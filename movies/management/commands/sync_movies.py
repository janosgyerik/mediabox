import os
import urllib2
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import simplejson as json
from django.db.utils import IntegrityError

from movies.models import File, Movie, MovieFile, Tag, MovieTag


def next_movie_file(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # todo: match against extension
            yield os.path.join(dirpath, filename)


def import_movie_file(path):
    filename = os.path.basename(path)
    basename, filetype = os.path.splitext(filename)
    stat = os.stat(path)
    cdate = datetime.fromtimestamp(stat.st_ctime)
    mdate = datetime.fromtimestamp(stat.st_mtime)
    mfile = File(
            path=path,
            filename=filename,
            orig_filename=filename,
            filetype=filetype,
            filesize=0,
            cdate=cdate,
            mdate=mdate,
            )
    try:
        mfile.save()
    except IntegrityError:
        pass


baseurl = 'http://www.omdbapi.com/?'

def fetch_imdb_info():
    for mfile in File.objects.filter(moviefile__isnull=True):
        if not mfile.cached_query_result:
            title, tmp = os.path.splitext(mfile.filename)
            url = '%st=%s' % (baseurl, title)
            response = urllib2.urlopen(url).read()
            mfile.cached_query_result = response
            mfile.save()
        info = json.loads(mfile.cached_query_result)
        print json.dumps(info, indent=4)
        if info['Response'] == 'True':
            movie = Movie(
                    title=info['Title'],
                    summary=info['Plot'],
                    year=info['Year'],
                    released=datetime.strptime(info['Released'], '%d %b %Y'),
                    runtime=info['Runtime'],
                    rated=info['Rated'],
                    source=baseurl,
                    )
            movie.save()
            MovieFile(file=mfile, movie=movie).save()
            for genre in info['Genre'].split(', '):
                try:
                    tag = Tag.objects.get(category='imdb', name=genre)
                except Tag.DoesNotExist:
                    tag = Tag(category='imdb', name=genre)
                    tag.save()
                try:
                    MovieTag(movie=movie, tag=tag).save()
                except IntegrityError:
                    pass
        break


class Command(BaseCommand):
    help = 'Synchronize movies data between the filesystem and the database'

    def handle(self, *args, **options):
        for path in args:
            if os.path.isdir(path):
                for path in next_movie_file(path):
                    import_movie_file(path)
                fetch_imdb_info()


# eof
