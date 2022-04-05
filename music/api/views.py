from rest_framework import generics
from ..models import (
    Genre,
)
from .serializers import (
    GenreListSerializer,
)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer