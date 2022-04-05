from django.core.files import File
from unittest import mock
from django.test import TestCase
from artist.tests.factory import ArtistFactory
from.factory import (
    GenreFactory,
    SongFactory,
    AlbumFactory,
)
from music.models import (
    Album,
    Song,
    Subtitle,
)

class SongTest(TestCase):

    def setUp(self):
        image = mock.MagicMock(spec=File) #  mocking imagefield
        image.name = "test.png"

        artist = ArtistFactory(name="nf")
        genre = GenreFactory(name="rap")
        album = AlbumFactory(name="the search",artist=artist)
        self.song = Song.objects.create(
            name = "nf",
            genre = genre,
            image = image,
            album = album,
        )
        self.song.artist.add(artist)
    
    def test_created(self):
        self.assertEqual(self.song.name, "nf")
        artist = self.song.artist.all()[0]
        self.assertEqual(artist.name, "nf")
        self.assertEqual(self.song.album.name, "the search")
        self.assertEqual(self.song.genre.name, "rap")
        self.assertTrue(self.song.image)
        self.assertEqual(str(self.song), "nf")


class SubtitleTest(TestCase):

    def setUp(self):
        # mocking open function in save method of Subtitle class
        mock_open = mock.mock_open()   
        with mock.patch("builtins.open", mock_open):
            with open("test.srt") as mock_f:
                mock_f.read.return_value = "subtitle text" # value returned to fill in Subtitle.text

                song = SongFactory(name="nf")
                self.subtitle = Subtitle(
                    song = song,
                    file = "test.srt",
                    language = "P",
                )
                self.subtitle.save()
    
    def test_created(self):
        self.assertEqual(self.subtitle.song.name, "nf")
        self.assertEqual(self.subtitle.language, "P")
        self.assertEqual(self.subtitle.text, "subtitle text")
        self.assertFalse(self.subtitle.file) # file deleted after reading in save method


class AlbumTest(TestCase):

    def setUp(self):
        artist = ArtistFactory(name="nf")
        genre = GenreFactory(name="rap")
        self.album = Album(
            name = "the search",
            artist = artist,
            genre = genre,
        )
        self.album.save()
        self.song = SongFactory(name="the search",album=self.album)
    
    def test_created(self):
        self.assertEqual(self.album.name, "the search")
        self.assertEqual(self.album.artist.name, "nf")
        self.assertEqual(self.album.genre.name, "rap")
        self.assertEqual(self.album.total_songs, 1)
        self.assertTrue(self.song in self.album.get_songs())