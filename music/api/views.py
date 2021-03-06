from django_filters import rest_framework as filters
from rest_framework import (
    generics,
    permissions,
)
from .paginations import SongPagination
from .permissions import IsPlayListOwner, IsLikeOwner
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
    PlayListUpdateSerializer,
    PlayListCreateSerializer,
    PlayListListSerializer,
    PlayListDetailSerializer,
    LikeCreateSerializer,
    LikeListSerializer,
)
from .filters import SongFilter


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


class SongDetailView(generics.RetrieveAPIView):
    queryset = Song.objects.select_related("album","genre")
    serializer_class = SongDetailSerializer


class SongListView(generics.ListAPIView):
    queryset = Song.objects.with_prefetch().with_views().order_by("-views_count")
    serializer_class = SongListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SongFilter
    pagination_class = SongPagination

class SubtitleDetailView(generics.RetrieveAPIView):
    queryset = Subtitle.objects.all()
    serializer_class = SubtitleDetailSerializer


class AlbumDetailView(generics.RetrieveAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumDetailSerializer


class ViewCreateView(generics.CreateAPIView):
    queryset = View.objects.all()
    serializer_class = ViewSerializer


class LikeListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return LikeCreateSerializer
        return LikeListSerializer


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = [IsLikeOwner, permissions.IsAuthenticated]


class PlayListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayList.objects.select_related("user").prefetch_related("songs")
    permission_classes = [IsPlayListOwner, permissions.IsAuthenticated]
        
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return PlayListUpdateSerializer
        return PlayListDetailSerializer

class PlayListCreateView(generics.ListCreateAPIView):
    
    def get_queryset(self):
        return PlayList.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PlayListCreateSerializer
        return PlayListListSerializer