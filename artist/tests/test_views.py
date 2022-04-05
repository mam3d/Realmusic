from rest_framework.test import APITestCase
from django.urls import reverse
from music.tests.factory import GenreFactory
from .factory import ArtistFactory

class ArtistListViewTest(APITestCase):
    def setUp(self):
        genre = GenreFactory(name="Rap")
        self.artist = ArtistFactory(name="nf", genre=genre)
        self.url = reverse("artist-list")

    def test_response(self):
        response = self.client.get(self.url)
        response_data = response.data[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], self.artist.name)
        self.assertEqual(response_data["genre"], "Rap")