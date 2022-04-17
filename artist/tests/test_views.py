from rest_framework.test import APITestCase
from django.urls import reverse
from user.tests.factory import UserFactory
from music.tests.factory import GenreFactory, SongFactory
from .factory import ArtistFactory


class ArtistListViewTest(APITestCase):
    def setUp(self):
        genre = GenreFactory(name="Rap")
        self.artist = ArtistFactory(name="nf", genre=genre)
        self.url = reverse("artist-list")

        self.user = UserFactory()
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_response(self):
        response = self.client.get(self.url, **self.authorization_header)
        response_data = response.data[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], self.artist.name)
        self.assertEqual(response_data["id"], self.artist.id)


class ArtistDetailViewTest(APITestCase):
    def setUp(self):
        genre = GenreFactory(name="Rap")
        self.artist = ArtistFactory(name="nf", genre=genre)
        song = SongFactory(name="the search")
        song.artists.add(self.artist)
        self.url = reverse("artist-detail",kwargs={"pk":self.artist.id})

        self.user = UserFactory()
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_response(self):
        response = self.client.get(self.url, **self.authorization_header)
        response_data = response.data
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], self.artist.name)
        self.assertEqual(response_data["albums"], [])
        self.assertEqual(self.artist.get_single_songs()[0].name, response_data["single_songs"][0]["name"])