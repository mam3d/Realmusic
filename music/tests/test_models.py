from django.core.files import File
from unittest import mock
from django.test import TestCase
from artist.tests.factory import ArtistFactory
from user.tests.factory import UserFactory
from.factory import (
    GenreFactory,
    SongFactory,
    AlbumFactory,
    ViewFactory,
)
from music.models import (
    Album,
    Song,
    Subtitle,
    View,
    PlayList,
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
            download_url = "t.com"
        )
        view = ViewFactory(song=self.song, user=UserFactory())
        self.song.artist.add(artist)
    
    def test_created(self):
        self.assertEqual(self.song.name, "nf")
        self.assertEqual(self.song.download_url, "t.com")
        artist = self.song.artist.all()[0]
        self.assertEqual(artist.name, "nf")
        self.assertEqual(self.song.album.name, "the search")
        self.assertEqual(self.song.genre.name, "rap")
        self.assertEqual(self.song.total_views, 1)
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


class ViewTest(TestCase):

    def setUp(self):
        user = UserFactory(username="test")
        song = SongFactory(name="the search")
        self.view = View.objects.create(user=user, song=song)

    
    def test_created(self):
        self.assertEqual(self.view.user.username, "test")
        self.assertEqual(self.view.song.name, "the search")
        self.assertEqual(str(self.view), "test-the search view")


class PlayListTest(TestCase):

    def setUp(self):
        user = UserFactory(username="test")
        self.song = SongFactory(name="the search")
        self.playlist = PlayList.objects.create(name="my-play-list", user=user)
        self.playlist.songs.add(self.song)

    
    def test_created(self):
        self.assertEqual(self.playlist.name, "my-play-list")
        self.assertEqual(self.playlist.image.name, "playlist/default.png")
        self.assertEqual(self.playlist.user.username, "test")
        self.assertTrue(self.song in self.playlist.songs.all())
        self.assertEqual(str(self.playlist), "test-my-play-list playlist")