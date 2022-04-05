from factory.django import DjangoModelFactory
from ..models import (
    Genre,
    Song,
    Album,
)

class GenreFactory(DjangoModelFactory):
    name = None
    
    class Meta:
        model = Genre

class SongFactory(DjangoModelFactory):
    name = None
    album = None
    class Meta:
        model = Song

class AlbumFactory(DjangoModelFactory):
    name = None
    artist = None
    genre = None
    class Meta:
        model = Album
