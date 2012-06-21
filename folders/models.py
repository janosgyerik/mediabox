from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=80)


class Artist(models.Model):
    name = models.CharField(max_length=80)
    genre = models.ForeignKey(Genre)


class Album(models.Model):
    title = models.CharField(max_length=80)
    artist = models.ForeignKey(Artist)
    release_date = models.DateTimeField()
    num_tracks = models.IntegerField(help_text='Number of tracks')


class AlbumSong(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    album = models.ForeignKey(Album)
    track = models.IntegerField()


class Single(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist)
    release_date = models.DateTimeField()


# eof
