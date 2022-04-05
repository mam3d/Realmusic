from django.urls import path
from .views import (
    GenreListView,
)

urlpatterns = [
    path("genres/", GenreListView.as_view(), name="genres"),
]
