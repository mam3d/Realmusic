from django.db.models import QuerySet
from django.db.models import Count

class SongManager(QuerySet):
    def with_views(self):
        return self.annotate(views_count=Count("views"))

    def with_prefetch(self):
        return self.prefetch_related("artists", "likes")