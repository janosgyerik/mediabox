from django.db import models


class Genre:
    name = models.CharField(max_length=80)


class Artist:
    name = models.CharField(max_length=80)
    genre = models.ForeignKey(Genre)


class Album:
    title = models.CharField(max_length=80)
    artist = models.ForeignKey(Artist)
    release_date = models.DateTimeField()
    num_tracks = models.IntegerField(help='Number of tracks')


class AlbumSong:
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album)
    track = models.IntegerField()


class Single:
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist)
    release_date = models.DateTimeField()


# eof
