from django.db import models
from django.utils import timezone


class File(models.Model):
    path = models.CharField(max_length=200, unique=True)
    filename = models.CharField(max_length=100)
    orig_filename = models.CharField(max_length=100)
    filetype = models.CharField(max_length=20)
    filesize = models.IntegerField()
    quality = models.IntegerField(default=0)
    cdate = models.DateField()
    mdate = models.DateField()

    def __unicode__(self):
        return '%s %s' % (self.filename, self.filesize)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    year = models.IntegerField()
    released = models.DateField()
    runtime = models.CharField(max_length=20)
    rated = models.CharField(max_length=20)
    homepage = models.URLField()
    source = models.CharField(max_length=20)

    def add_tag(self, name):
        pass

    def delete_tag(self, name):
        pass


class MovieFile(models.Model):
    file = models.ForeignKey(File)
    movie = models.ForeignKey(Movie)

    class Meta:
        unique_together = (('file', 'movie',),)


class Tag(models.Model):
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    class Meta:
        unique_together = (('category', 'name',),)


class MovieTag(models.Model):
    movie = models.ForeignKey(Movie)
    tag = models.ForeignKey(Tag)

    class Meta:
        unique_together = (('movie', 'tag',),)


class ImdbInfo(models.Model):
    movie = models.ForeignKey(Movie)
    imdb_id = models.CharField(max_length=50, unique=True)
    imdb_url = models.URLField()
    rating = models.FloatField()
    votes = models.IntegerField()
    created_dt = models.DateField(default=timezone.now)
    updated_dt = models.DateField(default=timezone.now)


class QueryCache(models.Model):
    file = models.ForeignKey(File)
    source = models.CharField(max_length=20)
    url = models.URLField()
    result = models.TextField()
    created_dt = models.DateField(default=timezone.now)
    updated_dt = models.DateField(default=timezone.now)

    class Meta:
        unique_together = (('file', 'source',),)


'''
class MovieDirector(models.Model):
    pass

class MovieWriter(models.Model):
    pass

class MovieActor(models.Model):
    pass

class MoviePoster(models.Model):
    pass
'''


# eof
