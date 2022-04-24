from django.db.models import Manager
from django.db.models import Count

class SongManager(Manager):
    def with_views(self):
        return self.get_queryset().annotate(views_count=Count("views"))