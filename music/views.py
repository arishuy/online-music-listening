from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def music(request):
    return HttpResponse("Hello, world. You're at the music index.")

def homepage(request):
    return render(request, 'homepage.html')
def recent(request):
    return render(request, 'recentlisten.html')

def playlists(request):
    return render(request, 'playlists.html')

def detail(request, song_id):
    return render(request, 'detailsong.html', {'song_id': song_id})