from factory.django import DjangoModelFactory
from ..models import Artist

class ArtistFactory(DjangoModelFactory):
    name = None
    genre = None
    class Meta:
        model = Artist