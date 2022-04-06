from django.urls import reverse
from rest_framework.test import APITestCase
from artist.tests.factory import ArtistFactory
from .factory import (
    GenreFactory,
    SongFactory,
    AlbumFactory,
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