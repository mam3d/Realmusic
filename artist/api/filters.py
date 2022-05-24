
import django_filters
from django_filters import rest_framework as filters
from artist.models import Artist

class ArtistFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Artist
        fields = ["name", "genre"]
