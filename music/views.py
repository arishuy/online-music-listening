import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Playlist
from .models import Song

# Create your views here.


def music(request):
    return HttpResponse("Hello, world. You're at the music index.")


def homepage(request):
    songs = Song.objects.all()
    print(songs)
    songJson = list(map(lambda song: {
        "name": song.name,
        "artists": list(map(lambda artist: {
            "name": artist.name
        }, song.artists.all())),
        "audio": song.audio_file.url if song.audio_file else song.audio_link,
    }, songs))
    return render(request, 'homepage.html', {'songs': json.dumps(songJson)})


def recent(request):
    return render(request, 'recentlisten.html')


def playlists(request):
    # get by user
    playlists = Playlist.objects.filter(owner=request.user).values()
    context = {
        'playlists': playlists,
    }
    return render(request, 'playlists.html', context)


def detail(request, song_id):
    return render(request, 'detailsong.html', {'song_id': song_id})


def detail_playlist(request, playlist_id):
    # get all song in playlist
    query = Playlist.objects.get(id=playlist_id)
    songs = query.song_list.all().values()
    context = {
        'songs': songs,
    }
    return render(request, 'detailplaylist.html', context)
