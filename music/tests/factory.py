from factory.django import DjangoModelFactory
from ..models import (
    Genre,
    Song,
    Album,
    Subtitle,
    View,
    PlayList,
)


class GenreFactory(DjangoModelFactory):
    name = None
    
    class Meta:
        model = Genre


class SongFactory(DjangoModelFactory):
    name = None
    album = None
    genre = None
    download_url = "t.com"
    class Meta:
        model = Song


class AlbumFactory(DjangoModelFactory):
    name = None
    artist = None
    genre = None
    class Meta:
        model = Album


class SubtitleFactory(DjangoModelFactory):
    song = None
    language = "P"
    text = "default text"
    class Meta:
        model = Subtitle


class ViewFactory(DjangoModelFactory):
    user = None
    song = None
    
    class Meta:
        model = View


class PlayListFactory(DjangoModelFactory):
    user = None
    name = None
    
    class Meta:
        model = PlayList