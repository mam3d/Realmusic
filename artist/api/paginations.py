from rest_framework.pagination import LimitOffsetPagination
from music.models import Artist

class ArtistPagination(LimitOffsetPagination):
    def get_count(self, queryset):
        return Artist.objects.count()