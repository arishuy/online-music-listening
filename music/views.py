import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import generic
from .models import Song
import random
from .models import Playlist
from .models import Song
from .models import Genre

# Create your views here.


def music(request):
    return HttpResponse("Hello, world. You're at the music index.")


def homepage(request):
    songs = Song.objects.all()
    # print(songs)
    songJson = list(map(lambda song: {
        "id": song.id,
        "name": song.name,
        "cover_path": song.cover_path,
        "artists": list(map(lambda artist: {
            "name": artist.name
        }, song.artists.all())),
        "audio": song.audio_file.url if song.audio_file else song.audio_link,
    }, songs))
    latest_songs = Song.objects.order_by('-release_day')[:5]
    random_count = 5
    if len(songs) < random_count:
        random_count = len(songs)
    suggested_songs = random.sample(list(songs), k=random_count)
    return render(request, 'homepage.html', {'songs': json.dumps(songJson), 'latest_songs': latest_songs, 'suggested_songs': suggested_songs})


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

def search(request):
    allgenres = Genre.objects.all()
    listgenre = list(map(lambda genre: {
        "id": genre.id,
        "name": genre.name,
    }, allgenres))
    context = {
        'allgenres': json.dumps(listgenre),
    }
    return render(request, 'search.html', context)
