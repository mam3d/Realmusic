import datetime
from django.db.models import Count
import django_filters
from django_filters import rest_framework as filters
from music.models import Song


class SongFilter(filters.FilterSet):
    top_month = django_filters.BooleanFilter(method="top_month_filter")
    top_week = django_filters.BooleanFilter(method="top_week_filter")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Song
        fields = ["name"]

    def top_month_filter(self, queryset, name, value):
        if value:
            start_date = datetime.date.today()
            month_ago = start_date - datetime.timedelta(days=30) 
            # filter based on number of views in last 30 days
            queryset = queryset.filter(views__date__gte=month_ago, views__date__lte=start_date).annotate(views_count=Count("views"))
            if len(queryset) > 10:
                return queryset.order_by("-views_count")[:11]
            return queryset.order_by("-views_count")

    def top_week_filter(self, queryset, name, value):
        if value:
            start_date = datetime.date.today()
            week_ago = start_date - datetime.timedelta(days=7) 
            # filter based on number of views in last 7 days
            queryset = queryset.filter(views__date__gte=week_ago, views__date__lte=start_date).annotate(views_count=Count("views"))
            if len(queryset) > 10:
                return queryset.order_by("-views_count")[:11]
            return queryset.order_by("-views_count")