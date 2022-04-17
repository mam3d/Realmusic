from django.test import TestCase
from music.tests.factory import SongFactory, AlbumFactory
from artist.models import Artist

class ArtistTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name="xxx tentacion")
        self.song = SongFactory(name="the search")
        self.song.artists.add(self.artist)
        self.album = AlbumFactory(name="the search", artist=self.artist)

    def test_created(self):
        self.assertEqual(self.artist.name, "xxx tentacion")
        self.assertEqual(self.artist.slug, "xxx-tentacion")
        self.assertTrue(self.song in self.artist.get_songs())
        self.assertTrue(self.album in self.artist.get_albums())
