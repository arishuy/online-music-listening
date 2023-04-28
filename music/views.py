import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from .models import Song, Playlist, Genre, ListenHistory, Album
import random

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from datetime import datetime
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
    }, songs.order_by('-release_day')))
    latest_songs = Song.objects.order_by('-release_day')[:10]
    random_count = 5
    if len(songs) < random_count:
        random_count = len(songs)
    suggested_songs = random.sample(list(songs), k=random_count)

    latest_albums = Album.objects.order_by('-release_day')
    context = {
        'songs': json.dumps(songJson),
        'latest_songs': latest_songs,
        'suggested_songs': suggested_songs,
        'latest_albums': latest_albums
    }
    return render(request, 'homepage.html', context)

def recent(request):
    user = request.user
    if user.id is not None:
        recent_listen = ListenHistory.objects.filter(owner__id=user.id).order_by('-stream_date')[:10]
        recent_listenJson = list(map(lambda recent: {
            "id": recent.song.id,
            "name": recent.song.name,
            "cover_path": recent.song.cover_path,
            "artists": list(map(lambda artist: {
                "name": artist.name
            }, recent.song.artists.all())),
            "audio": recent.song.audio_file.url if recent.song.audio_file else recent.song.audio_link,
        }, recent_listen))
        return render(request, 'recentlisten.html', {'recent_listen': recent_listen, 'songs': json.dumps(recent_listenJson)})
    else:
        return HttpResponseRedirect(reverse('homepage'))


def playlists(request):
    # get by user
    playlists = Playlist.objects.filter(owner=request.user).values()
    context = {
        'playlists': playlists,
    }
    return render(request, 'playlists.html', context)


def detail(request, song_id):
    song = Song.objects.get(id=song_id)
    songJson = {
        "id": song.id,
        "audio": song.audio_file.url if song.audio_file else song.audio_link,
    }
    songJson = json.dumps(songJson)
    return render(request, 'detailsong.html', {'song': song, 'songJson': songJson})


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
        'allgenres': listgenre,
    }
    if request.method == "POST":
        genre_id = request.POST["genre"]
        text = request.POST["text"]
        songs = Song.objects.filter(
            genres__id__contains=genre_id).filter(name__contains=text)
        context["text"] = text
        context["genre_id"] = int(genre_id)
        context["songs"] = songs
        return render(request, 'search.html', context)

    return render(request, 'search.html', context)


@csrf_exempt
def stream(request):
    if request.method == 'POST':
        song_id = request.POST['song_id']
        if request.user.id is not None:
            listen_history = ListenHistory.objects.create(stream_date=datetime.now(), owner=User(id=request.user.id), song=Song(id=song_id))
            listen_history.save()
        song = Song.objects.get(id=song_id)
        # using F class to avoid race condition
        song.stream_count = F('stream_count') + 1
        song.save()
        
        return HttpResponse('success')
    else:
        return HttpResponse('unsuccessful')