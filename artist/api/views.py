from rest_framework import (
    generics,
    permissions,
    viewsets,
    pagination
)
from .filters import ArtistFilter
from ..models import Artist, Follow
from .serializers import (
    ArtistListSerializer,
    ArtistDetailSerializer,
    FollowCreateSerializer,
    FollowingSerializer,
)
from .permissions import IsFollowOwner


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    filterset_class = ArtistFilter
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return ArtistListSerializer
        return ArtistDetailSerializer


class FollowView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return  FollowCreateSerializer
        return FollowingSerializer

class FollowDeleteView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    permission_classes = [IsFollowOwner, permissions.IsAuthenticated]

