from django.shortcuts import render
from django.http import HttpResponse
from .models import Playlist

# Create your views here.

def music(request):
    return HttpResponse("Hello, world. You're at the music index.")

def homepage(request):
    return render(request, 'homepage.html')
def recent(request):
    return render(request, 'recentlisten.html')

def playlists(request):
    # get by user
    playlists = Playlist.objects.filter(owner=request.user).values()
    context = {
        'playlists': playlists,
    }
    return render(request, 'playlists.html' , context)

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