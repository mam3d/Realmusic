from django.urls import path
from .views import (
    GenreListView,
    SongDetailView,
    SongListView,
    SubtitleDetailView,
    AlbumDetailView,
    ViewCreateView,
    PlayListView,
    PlayListCreateView,
    LikeCreateView,
)

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
    path("playlist/<int:pk>/", PlayListView.as_view(), name="playlist"),
    path("playlist/", PlayListCreateView.as_view(), name="playlist-create"),
    path("view/", ViewCreateView.as_view(), name="view-create"),
    path("like/", LikeCreateView.as_view(), name="like-create"),
    path("song/", SongListView.as_view(), name="song"),
    path("song/<int:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("subtitle/<int:pk>/", SubtitleDetailView.as_view(), name="subtitle-detail"),
    path("album/<int:pk>/", AlbumDetailView.as_view(), name="album-detail"),
]

