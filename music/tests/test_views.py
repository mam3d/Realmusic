from django.urls import reverse
from rest_framework.test import APITestCase
from artist.tests.factory import ArtistFactory
from .factory import (
    GenreFactory,
    SongFactory,
    AlbumFactory,
    SubtitleFactory,
)

class GenreListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("genres")
        self.genre = GenreFactory(name="Rap")

    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], self.genre.name)
        self.assertEqual(response.data[0]["id"], self.genre.id)


class SongDetailViewTest(APITestCase):
    def setUp(self):
        self.artist = ArtistFactory(name="nf")
        self.album = AlbumFactory(name="the search",artist=self.artist)
        self.genre = GenreFactory(name="Rap")
        self.song = SongFactory(
            name="the search",
            album=self.album,
            genre=self.genre,
            )
        self.url = reverse("song-detail",kwargs={"pk":self.song.id})


    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.song.name)
        self.assertEqual(response.data["album"], self.album.name)
        self.assertEqual(response.data["genre"], self.genre.name)
        self.assertEqual(response.data["download_url"], self.song.download_url)


class SubtitleDetailViewTest(APITestCase):
    def setUp(self):
        self.song = SongFactory(name="the search")
        self.subtitle = SubtitleFactory(song=self.song)
        self.url = reverse("subtitle-detail", kwargs={"pk":self.subtitle.id})

    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["language"], "Persian")
        self.assertEqual(response.data["text"], "default text")
        self.assertEqual(response.data["id"], self.subtitle.id)


class AlbumDetailViewTest(APITestCase):
    def setUp(self):
        artist = ArtistFactory(name="nf")
        genre = GenreFactory(name="Rap")
        self.album = AlbumFactory(name="the search",artist=artist, genre=genre)
        song = SongFactory(
            name="the search",
            album=self.album,
            genre=genre,
            )
        self.url = reverse("album-detail",kwargs={"pk":self.album.id})


    def test_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.album.id)
        self.assertEqual(response.data["name"], "the search")
        self.assertEqual(response.data["genre"], "Rap")
        self.assertEqual(response.data["total_songs"], 1)