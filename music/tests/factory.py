from factory.django import DjangoModelFactory
from artist.models import Artist
from ..models import (
    Genre,
    Song,
    Album,
)

class ArtistFactory(DjangoModelFactory):
    name = None

    class Meta:
        model = Artist

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
    class Meta:
        model = Album
