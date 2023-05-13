from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=2000)
    cover_path = models.ImageField(
        blank=True, null=True, upload_to='artist_cover/')

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
    cover_path = models.ImageField(null=True, upload_to='album_cover/')

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=100)
    stream_count = models.IntegerField(default=0)
    cover_path = models.ImageField(
        blank=True, null=True, upload_to='song_cover/')
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

    def artist_list_str(self) -> str:
        result = []
        for artist in self.artists.all():
            result.append(artist.name)

        return ', '.join(result)

    def get_cover_path(self) -> str:
        if not self.cover_path:
            return self.album.cover_path.url
        else:
            return self.cover_path.url


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    song_list = models.ManyToManyField(Song, related_name='song_playlists')
    create_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class ListenHistory(models.Model):
    stream_date = models.DateTimeField()
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.song.name
