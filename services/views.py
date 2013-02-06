from django.contrib.auth.models import User
from explorer.models import Genre, Artist, Album, AlbumSong, Single

from services.handler import model_service


def user_service(request, url):
    return model_service(User, request, url, include=['id', 'username'])


def genre_service(request, url):
    return model_service(Genre, request, url)


def artist_service(request, url):
    return model_service(Artist, request, url)


def album_service(request, url):
    return model_service(Album, request, url)


def albumsong_service(request, url):
    return model_service(AlbumSong, request, url)


def single_service(request, url):
    return model_service(Single, request, url)


# eof
