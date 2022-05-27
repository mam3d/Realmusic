from django.db.models import Count
from rest_framework import (
    generics,
    permissions,
    viewsets,
)
from .paginations import ArtistPagination
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
    queryset = Artist.objects.annotate(total_followers=Count("followers")).order_by("-total_followers")
    filterset_class = ArtistFilter
    pagination_class = ArtistPagination

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

