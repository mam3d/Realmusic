from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Artist
from .serializers import (
    ArtistListSerializer,
    ArtistDetailSerializer,
)

class ArtistViewSet(ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["genre"]
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return ArtistListSerializer
        return ArtistDetailSerializer