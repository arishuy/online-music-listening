from django.urls import path
from . import views

urlpatterns = [
    path('music/', views.music, name='music'),
    path('', views.homepage, name='hompage'),
    path('recent/', views.recent, name='recent'),
    path('playlists/', views.playlists, name='playlists'),
]