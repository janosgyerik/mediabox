import os
import sys
from datetime import datetime
from mutagen.easyid3 import EasyID3

from django.conf import settings

from folders.models import Genre, Artist, Album, AlbumSong


def _print(*args):
    try:
        print ' '.join([unicode(x) for x in args])
    except:
        print ' '.join([str(x) for x in args])


def info(*args):
    _print('[info]', *args)


def warning(*args):
    _print('[warning]', *args)


def error(*args):
    _print('[error]', *args)
    sys.exit(1)


def sync_music():
    for abspath, relpath in find_music_files():
        info('importing file: %s' % relpath)
        audioinfo = get_audioinfo(abspath)
        if audioinfo is not None:
            genre = get_genre_by_name(audioinfo['genre'])
            artist = get_or_create_artist(audioinfo['artist'], genre)


def find_music_files():
    """ returns absolute paths of music files under settings.MUSIC_ROOT """
    path = settings.MUSIC_ROOT

    for root, dirs, files in os.walk(path):
        for filename in files:
            abspath = os.path.join(root, filename)
            relpath = abspath.replace(settings.MUSIC_ROOT, '')
            yield (abspath, relpath)


def get_audioinfo(filepath):
    audioinfo = None
    if filepath.endswith('.mp3'):
        audioinfo = get_audioinfo_by_easyid3(EasyID3(filepath))

    return audioinfo


def get_audioinfo_by_easyid3(easyid3):
    (track, num_tracks) = easyid3['tracknumber'][0].split('/')
    released_date = datetime(int(easyid3['date'][0]), 1, 1)
    return {
            'artist': easyid3['artist'][0],
            'genre': easyid3['genre'][0],
            'album': easyid3['album'][0],
            'title': easyid3['title'][0],
            'track': track,
            'num_tracks': num_tracks,
            'released_date': released_date,
            }


def get_genre_by_name(name):
    return Genre.objects.get(name=name)


def get_or_create_artist(name, genre):
    try:
        return Artist.objects.get(name=name)
    except Artist.DoesNotExist:
        artist = Artist(name=name, genre=genre)
        artist.save()
        return artist


# eof
