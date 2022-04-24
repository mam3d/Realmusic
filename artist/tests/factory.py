from factory.django import DjangoModelFactory
from ..models import Artist, Follow

class ArtistFactory(DjangoModelFactory):
    name = None
    genre = None
    class Meta:
        model = Artist


class FollowFactory(DjangoModelFactory):
    user = None
    artist = None
    class Meta:
        model = Follow