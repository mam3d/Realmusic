from django.urls import path
from .views import (
    GenreListView,
    SongDetailView,
    SubtitleDetailView,
    AlbumDetailView,
)

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
    path("<int:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("subtitle/<int:pk>/", SubtitleDetailView.as_view(), name="subtitle-detail"),
    path("album/<int:pk>/", AlbumDetailView.as_view(), name="album-detail"),
]
