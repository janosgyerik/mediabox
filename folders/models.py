from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=80)
    id3_id = models.IntegerField()
    created_dt = models.DateTimeField(auto_now_add=True, blank=True)


class Artist(models.Model):
    name = models.CharField(max_length=80)
    genre = models.ForeignKey(Genre)
    created_dt = models.DateTimeField(auto_now_add=True, blank=True)
    updated_dt = models.DateTimeField(auto_now_add=True, blank=True)


class Album(models.Model):
    title = models.CharField(max_length=80)
    artist = models.ForeignKey(Artist)
    release_date = models.DateTimeField()
    num_tracks = models.IntegerField(help_text='Number of tracks')
    created_dt = models.DateTimeField(auto_now_add=True, blank=True)
    updated_dt = models.DateTimeField(auto_now_add=True, blank=True)


class AlbumSong(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    album = models.ForeignKey(Album)
    track = models.IntegerField()
    created_dt = models.DateTimeField(auto_now_add=True, blank=True)
    updated_dt = models.DateTimeField(auto_now_add=True, blank=True)


class Single(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist)
    release_date = models.DateTimeField()
    created_dt = models.DateTimeField(auto_now_add=True, blank=True)
    updated_dt = models.DateTimeField(auto_now_add=True, blank=True)


# eof
