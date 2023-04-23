from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_day = models.DateField()

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=100)
    stream_count = models.IntegerField(default=0)
    image = models.CharField(max_length=100, default="")
    audio_file = models.FileField(blank=True, null=True, upload_to="audio/")
    audio_link = models.CharField(max_length=100, blank=True, null=True)
    release_day = models.DateField()
    duration = models.IntegerField()
    album = models.ForeignKey(
        Album, null=True, blank=True, on_delete=models.SET_NULL)
    artists = models.ManyToManyField(Artist)
    genres = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    song_list = models.ManyToManyField(Song)
    create_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
