from rest_framework import (
    filters,
    generics,
    permissions,
    viewsets,
)
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Artist, Follow
from .serializers import (
    ArtistListSerializer,
    ArtistDetailSerializer,
    FollowSerializer,
    FollowingSerializer,
)
from .permissions import IsFollowOwner


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["genre"]
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return ArtistListSerializer
        return ArtistDetailSerializer


class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    permission_classes = [IsFollowOwner, permissions.IsAuthenticated]


class FollowingView(generics.ListAPIView):
    serializer_class = FollowingSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)