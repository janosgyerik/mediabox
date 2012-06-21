import os
from mutagen.easyid3 import EasyID3

from django.conf import settings

#from folders.models import Artist, Album, AlbumSong


def sync_music():
    for abspath, relpath in find_music_files():
        audioinfo = get_audioinfo(abspath)
        audioinfo.pprint()
        print audioinfo.keys()
        print audioinfo['title']
        print audioinfo['artist']
        break


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
        audioinfo = EasyID3(filepath)

    return audioinfo


# eof
