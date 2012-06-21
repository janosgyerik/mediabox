import os
import mutagen
#from datetime import datetime

from django.conf import settings

#from folders.models import Artist, Album, AlbumSong


def sync_music():
    for filepath in find_music_files():
        audio = get_audio(filepath)


def find_music_files():
    """ returns absolute paths of music files under settings.MUSIC_ROOT """
    path = settings.MUSIC_ROOT

    for root, dirs, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            yield filepath


def get_audio(filepath):
    pass


# eof
