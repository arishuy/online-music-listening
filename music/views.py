from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Song
import random
# Create your views here.

def music(request):
    return HttpResponse("Hello, world. You're at the music index.")

# def homepage(request):
#     return render(request, 'homepage.html')
def homepage(request):
    latest_songs = Song.objects.order_by('-release_day')[:5]
    random_count = 5
    if len(Song.objects.all()) < random_count:
        random_count = len(Song.objects.all())
    suggested_songs = random.sample(list(Song.objects.all()), k=random_count)
    return render(request, 'homepage.html', {'latest_songs': latest_songs, 'suggested_songs': suggested_songs})

def recent(request):
    return render(request, 'recentlisten.html')

def playlists(request):
    return render(request, 'playlists.html')

def detail(request, song_id):
    return render(request, 'detailsong.html', {'song_id': song_id})