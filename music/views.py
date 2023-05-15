import json
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import generic
from .models import Song, Playlist, Genre, ListenHistory, Album, Artist
import random
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from datetime import datetime
# Create your views here.


def music(request):
    return HttpResponse("Hello, world. You're at the music index.")


def homepage(request):
    # get avatar user from Userinfo

    songs = Song.objects.all()
    songJson = get_songJson(songs.order_by('-release_day'))
    latest_songs = Song.objects.order_by('-release_day')[:10]
    random_count = 5
    if len(songs) < random_count:
        random_count = len(songs)
    suggested_songs = random.sample(list(songs), k=random_count)

    latest_albums = Album.objects.order_by('-release_day')
    context = {
        'songJson': json.dumps(songJson),
        'latest_songs': latest_songs,
        'suggested_songs': suggested_songs,
        'latest_albums': latest_albums,

    }
    return render(request, 'homepage.html', context)


def album(request, album_id):

    album = Album.objects.get(id=album_id)
    songs = Song.objects.filter(album__id=album_id)
    songJson = get_songJson(songs)
    context = {
        'album': album,
        'songJson': json.dumps(songJson),
        'songs': songs,

    }
    return render(request, 'album.html', context)


def chart(request):

    # get 10 songs with highest listen count
    songs = Song.objects.order_by('-stream_count')[:10]
    print(songs[0])
    songJson = get_songJson(songs)
    context = {
        'songs': json.dumps(songJson),
        'songs': songs,

    }
    return render(request, 'chart.html', context)


def recent(request):

    user = request.user
    if user.id is not None:
        recent_listen = ListenHistory.objects.filter(
            owner__id=user.id).order_by('-stream_date')[:10]
        recent_listenJson = get_songJson(
            list(map(lambda x: x.song, recent_listen)))
        return render(request, 'recentlisten.html', {'recent_listen': recent_listen, 'songJson': json.dumps(recent_listenJson), })
    else:
        return HttpResponseRedirect(reverse('homepage'))


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
        newPlaylist.create_date = datetime.now()
        newPlaylist.owner = request.user
        newPlaylist.save()
        return JsonResponse({'message': 'success'})


def detail(request, song_id):

    song = Song.objects.get(id=song_id)
    songJson = get_songJson([song])
    songJson = json.dumps(songJson)
    return render(request, 'detailsong.html', {'song': song, 'songJson': songJson, })


def detail_playlist(request, playlist_id):

    # get all song in playlist
    query = Playlist.objects.get(id=playlist_id)
    songs = query.song_list.all()
    songJson = get_songJson(songs)
    context = {
        'playlist_id': playlist_id,
        'songs': songs,
        'songJson': json.dumps(songJson),

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
        if int(genre_id) != -1:
            songs = Song.objects.filter(
                genres__id=genre_id).filter(name__contains=text)
            context["text"] = text
            context["genre_id"] = int(genre_id)
            context["songs"] = songs

    return render(request, 'search.html', context)


@csrf_exempt
def stream(request):

    if request.method == 'POST':
        song_id = request.POST['song_id']
        if request.user.id is not None:
            listen_history = ListenHistory.objects.create(
                stream_date=datetime.now(), owner=User(id=request.user.id), song=Song(id=song_id))
            listen_history.save()
        song = Song.objects.get(id=song_id)
        # using F class to avoid race condition
        song.stream_count = F('stream_count') + 1
        song.save()

        return HttpResponse('success')
    else:
        return HttpResponse('unsuccessful')


@csrf_exempt
def playlistsBySong(request, song_id):

    if request.method == "GET" and request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user)
        song = Song.objects.get(pk=song_id)
        song_playlists = song.song_playlists.all()
        playlistsJson = list(map(lambda playlist: {
            "id": playlist.id,
            "name": playlist.name,
            "included": playlist in song_playlists
        }, playlists))
        return JsonResponse({'playlists': playlistsJson})

    if request.method == "POST" and request.user.is_authenticated:
        song = Song.objects.get(id=song_id)
        curr_song_playlists_id = set(
            map(lambda playlist: str(playlist['id']), song.song_playlists.all().values('id')))
        new_song_playlists_id = set(request.POST.getlist('playlists[]'))
        for playlist_id in curr_song_playlists_id.union(new_song_playlists_id):
            if playlist_id in curr_song_playlists_id.intersection(new_song_playlists_id):
                continue
            elif playlist_id in new_song_playlists_id:
                playlist = Playlist.objects.get(pk=playlist_id)
                playlist.song_list.add(song)
                playlist.save()
            else:
                playlist = Playlist.objects.get(pk=playlist_id)
                playlist.song_list.remove(song)
                playlist.save()
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'error'})


def artist(request, artist_id):

    artist = Artist.objects.get(pk=artist_id)
    songs = Song.objects.filter(artists__id=artist_id)
    popular_songs = songs.order_by('-stream_count')[:5]
    latest_albums = Album.objects.filter(
        artist__id=artist_id).order_by('-release_day')
    songJson = get_songJson(songs)
    context = {
        'artist': artist,
        'songs': songs,
        'popular_songs': popular_songs,
        'latest_albums': latest_albums,
        'songJson': json.dumps(songJson),

    }
    return render(request, 'artist.html', context)


def song_in_playlist(request, playlist_id, song_id):

    if request.method == 'POST':
        song = Song.objects.get(pk=song_id)
        playlist = Playlist.objects.get(pk=playlist_id)
        if song in playlist.song_list.all():
            playlist.song_list.remove(song)
            playlist.save()
        return HttpResponseRedirect(
            reverse('detail_playlist', args=(playlist_id,), context={

            }))
    return HttpResponseRedirect(
        reverse('detail_playlist', args=(playlist_id,),
                context={

        }))


def get_songJson(songs):
    return list(map(lambda song: {
        "id": song.id,
        "name": song.name,
        "cover_path": song.get_cover_path(),
        "artists": list(map(lambda artist: {
            "name": artist.name
        }, song.artists.all())),
        "audio": song.audio_file.url if song.audio_file else song.audio_link,
    }, songs))
