from rest_framework.viewsets import ReadOnlyModelViewSet
from ..models import Artist
from .serializers import (
    ArtistListSerializer,
    ArtistDetailSerializer,
)

class ArtistViewSet(ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    lookup_field = "slug"
    filterset_fields = ["genre"]

    def get_serializer_class(self):
        if self.action == "list":
            return ArtistListSerializer
        return ArtistDetailSerializer