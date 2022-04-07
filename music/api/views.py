from rest_framework import generics
from ..models import (
    Genre,
    Song,
    Subtitle,
    Album,
)
from .serializers import (
    GenreListSerializer,
    SongDetailSerializer,
    SubtitleDetailSerializer,
    AlbumDetailSerializer,
)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


class SongDetailView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongDetailSerializer


class SubtitleDetailView(generics.RetrieveAPIView):
    queryset = Subtitle.objects.all()
    serializer_class = SubtitleDetailSerializer

class AlbumDetailView(generics.RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumDetailSerializer