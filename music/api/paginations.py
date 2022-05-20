from rest_framework.pagination import LimitOffsetPagination
from music.models import Song

class SongPagination(LimitOffsetPagination):
    def get_count(self, queryset):
        return Song.objects.count()