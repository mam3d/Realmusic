from django.db.models import Count
from rest_framework import (
    generics,
    permissions,
    filters,
)
from .permissions import IsPlayListOwner
from ..models import (
    Genre,
    Song,
    Subtitle,
    Album,
    View,
    PlayList,
    Like,
)
from .serializers import (
    GenreListSerializer,
    SongDetailSerializer,
    SongListSerializer,
    SubtitleDetailSerializer,
    AlbumDetailSerializer,
    ViewSerializer,
    PlayListCreateUpdateSerializer,
    PlayListSerializer,
    LikeSerializer
)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


class SongDetailView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongDetailSerializer


class SongListView(generics.ListAPIView):
    queryset = Song.objects.annotate(views_count=Count("views")).order_by("-views_count")
    serializer_class = SongListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class SubtitleDetailView(generics.RetrieveAPIView):
    queryset = Subtitle.objects.all()
    serializer_class = SubtitleDetailSerializer


class AlbumDetailView(generics.RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumDetailSerializer


class ViewCreateView(generics.CreateAPIView):
    queryset = View.objects.all()
    serializer_class = ViewSerializer


class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class PlayListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayList.objects.all()
    permission_classes = [IsPlayListOwner, permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return PlayListCreateUpdateSerializer
        return PlayListSerializer


class PlayListCreateView(generics.CreateAPIView):
    queryset = PlayList.objects.all()
    serializer_class = PlayListCreateUpdateSerializer