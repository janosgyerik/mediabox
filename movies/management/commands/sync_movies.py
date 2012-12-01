import os
import urllib2
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import simplejson as json
from django.db.utils import IntegrityError

from movies.models import File, Movie, MovieFile, Tag, MovieTag
from movies.models import QueryCache

omdbapi_url = 'http://www.omdbapi.com/?'


def next_movie_file(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # todo: filter out junk, for example by extension
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


def get_omdbapi_info(mfile):
    source = 'omdbapi'
    try:
        cache = QueryCache.objects.get(file=mfile, source=source)
        rawinfo = cache.result
    except QueryCache.DoesNotExist:
        title, tmp = os.path.splitext(mfile.filename)
        url = omdbapi_url + 't=' + title
        rawinfo = urllib2.urlopen(url).read()
        QueryCache(
                file=mfile,
                source=source,
                url=url,
                result=rawinfo,
                ).save()
    rawinfo = json.loads(rawinfo)
    print json.dumps(rawinfo, indent=4)
    if rawinfo['Response'] == 'True':
        is_ok = True
        info = {
                'title': rawinfo['Title'],
                'summary': rawinfo['Plot'],
                'year': int(rawinfo['Year']),
                'runtime': rawinfo['Runtime'],
                'rated': rawinfo['Rated'],
                'source': source,
                'tags': [],
                }
        try:
            released = datetime.strptime(rawinfo['Released'], '%d %b %Y')
            info['released'] = released
        except ValueError:
            pass
        for genre in rawinfo['Genre'].split(', '):
            try:
                tag = Tag.objects.get(category=source, name=genre)
            except Tag.DoesNotExist:
                tag = Tag(category=source, name=genre)
                tag.save()
            info['tags'].append(tag)
    else:
        is_ok, info = False, None
    return is_ok, info


def import_new_movies():
    for mfile in File.objects.filter(moviefile__isnull=True):
        is_ok, info = get_omdbapi_info(mfile)
        if is_ok:
            import_movie(mfile, info)
        break


def import_movie(mfile, info):
    movie = Movie(
            title=info['title'],
            summary=info['summary'],
            year=info['year'],
            runtime=info['runtime'],
            rated=info['rated'],
            source=info['source'],
            )
    if 'released' in info:
        movie.released = info['released']
    movie.save()
    MovieFile(file=mfile, movie=movie).save()
    for tag in info['tags']:
        try:
            MovieTag(movie=movie, tag=tag).save()
        except IntegrityError:
            pass


class Command(BaseCommand):
    help = 'Synchronize movies data between the filesystem and the database'

    def handle(self, *args, **options):
        for path in args:
            if os.path.isdir(path):
                for path in next_movie_file(path):
                    import_movie_file(path)
                import_new_movies()


# eof