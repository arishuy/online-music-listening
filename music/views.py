import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Song
import random
from .models import Playlist
from .models import Song
from .models import Genre
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def playlists(request):
    # get by user
    if request.method == "GET" and request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user).values()
        context = {
            'playlists': playlists,
        }
        return render(request, 'playlists.html', context)
    if request.method == "POST" and request.user.is_authenticated:
        newPlaylist = Playlist()
        newPlaylist.name = request.POST["name"]
        newPlaylist.create_date = datetime.datetime.now()
        newPlaylist.owner = request.user
        newPlaylist.save()
        return JsonResponse({'message': 'success'})


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
def playlistsBySong(request, song_id):
    if request.method == "GET" and request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user)
        song_playlists = Playlist.objects.filter(
            owner=request.user).filter(song_list__id__contains=song_id)
        playlistsJson = list(map(lambda playlist: {
            "id": playlist.id,
            "name": playlist.name,
            "included": song_playlists.contains(playlist)
        }, playlists))
        return JsonResponse({'playlists': playlistsJson})

    if request.method == "POST" and request.user.is_authenticated:
        song = Song.objects.get(id=song_id)
        for playlist_id in request.POST.getlist('playlists[]'):
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.song_list.add(song)
            playlist.save()
        return JsonResponse({'message': 'success'})
