from django.test import TestCase
from music.tests.factory import SongFactory, AlbumFactory
from artist.models import Artist

class ArtistTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name="nf")
        self.song = SongFactory(name="the search")
        self.song.artist.add(self.artist)
        self.album = AlbumFactory(name="the search", artist=self.artist)
        print(self.artist.get_songs())

    def test_created(self):
        self.assertEqual(self.artist.name, "nf")
        self.assertTrue(self.song in self.artist.get_songs())
        self.assertTrue(self.album in self.artist.get_albums())
