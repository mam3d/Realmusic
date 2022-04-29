from rest_framework.test import APITestCase
from django.urls import reverse
from artist.models import Follow
from user.tests.factory import UserFactory
from music.tests.factory import GenreFactory, SongFactory
from .factory import ArtistFactory, FollowFactory


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
        song = SongFactory(name="the search", duration=1.55)
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


class FollowViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.artist = ArtistFactory(name="testing2")
        self.follow = FollowFactory(user=self.user, artist=self.artist)

        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_get(self):
        url = reverse("follow")
        response = self.client.get(url, **self.authorization_header)
        response_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]["artist"], self.artist.name)

    def test_create(self):
        url = reverse("follow")
        artist = ArtistFactory(name="eminem")
        payload = {
            "artist":artist.id
        }
        response = self.client.post(url, data=payload, **self.authorization_header)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Follow.objects.get(user=self.user, artist=artist))

    def test_delete(self):
        url = reverse("follow-delete", kwargs={"pk":int(f"{self.user.id}{self.artist.id}")})
        response = self.client.delete(url, **self.authorization_header)

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Follow.DoesNotExist):
            Follow.objects.get(user=self.user, artist=self.artist)
    