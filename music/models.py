from django.db import models

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
    link = models.CharField(max_length=100)
    release_day = models.DateField()
    duration = models.IntegerField()
    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.SET_NULL)
    artists = models.ManyToManyField(Artist)
    genres = models.ManyToManyField(Genre)


    def __str__(self) -> str:
        return self.name
    


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=30)


    def __str__(self) -> str:
        return self.username
    


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    song_list = models.ManyToManyField(Song)
    create_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.name