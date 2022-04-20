from django.urls import reverse
from rest_framework.test import APITestCase
from artist.tests.factory import ArtistFactory
from user.tests.factory import UserFactory
from music.models import PlayList, Like
from .factory import (
    GenreFactory,
    SongFactory,
    AlbumFactory,
    SubtitleFactory,
    ViewFactory,
    PlayListFactory,
)

class GenreListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("genres")
        self.genre = GenreFactory(name="Rap")

        self.user = UserFactory()
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_response(self):
        response = self.client.get(self.url, **self.authorization_header)
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

        self.user = UserFactory()
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_response(self):
        response = self.client.get(self.url, **self.authorization_header)
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

        self.user = UserFactory()
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_response(self):
        response = self.client.get(self.url, **self.authorization_header)
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

        self.user = UserFactory()
        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_response(self):
        response = self.client.get(self.url, **self.authorization_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.album.id)
        self.assertEqual(response.data["name"], "the search")
        self.assertEqual(response.data["genre"], "Rap")
        self.assertEqual(response.data["total_songs"], 1)


class ViewCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="nf")
        self.song = SongFactory(name="the search")
        self.url = reverse("view-create")

        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_response(self):
        payload = {
            "song":self.song.id,           
            }
        response = self.client.post(self.url, data=payload, **self.authorization_header)
        self.assertEqual(response.status_code, 201)

    def test_fails(self):
        payload = {
            "song":self.song.id,           
            }
        # already exists
        ViewFactory(user=self.user,song=self.song)
        response = self.client.post(self.url, data=payload, **self.authorization_header)
        self.assertEqual(response.status_code, 400)


class LikeViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="nf")
        self.song = SongFactory(name="the search")

        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_create(self):
        payload = {
            "song":self.song.id,           
            }
        url = reverse("like-create")
        response = self.client.post(url, data=payload, **self.authorization_header)
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        Like.objects.create(user=self.user, song=self.song)
        url = reverse("like-delete", kwargs={"pk":int(f"{self.user.id}{self.song.id}")})
        response = self.client.delete(url, **self.authorization_header)
        self.assertEqual(response.status_code, 204)


class PlayListViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="nf")
        self.song = SongFactory(name="the search")
        self.song2 = SongFactory(name="song2")
        self.playlist = PlayListFactory(name="test_playlist",user=self.user)
        self.playlist.songs.add(self.song)

        access = self.user.get_jwt_token()["access"]
        self.authorization_header = {"HTTP_AUTHORIZATION":f"Bearer {access}"}

    def test_delete(self):
        url = reverse("playlist", kwargs={"pk":self.playlist.id})
        response = self.client.delete(url, **self.authorization_header)
        self.assertEqual(response.status_code, 204)

    def test_get(self):
        url = reverse("playlist", kwargs={"pk":self.playlist.id})
        response = self.client.get(url, **self.authorization_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "test_playlist")
        self.assertEqual(response.data["user"], self.user.id)

    def test_put(self):
        url = reverse("playlist", kwargs={"pk":self.playlist.id})

        payload = {
            "name":"edited_playlist",
            "remove_songs":self.song.id, 
        }
        response = self.client.put(url, data=payload, **self.authorization_header)
        self.assertEqual(response.status_code, 200)
        playlist = PlayList.objects.get(id=self.playlist.id)
        self.assertEqual(playlist.name, "edited_playlist")
        self.assertFalse(playlist.songs.all())

        # test put with add_songs
        payload = {
            "name":"edited_playlist",
            "add_songs":self.song2.id, 
        }
        response = self.client.put(url, data=payload, **self.authorization_header)
        playlist = PlayList.objects.get(id=self.playlist.id)
        self.assertTrue(self.song2 in playlist.songs.all())

        # test put with clear_songs
        payload.update(clear_songs=True)
        response = self.client.put(url, data=payload, **self.authorization_header)
        playlist = PlayList.objects.get(id=self.playlist.id)
        self.assertFalse(playlist.songs.all())

    def test_create(self):
        url = reverse("playlist-create")
        payload = {
            "name":"test_playlist",
        }
        response = self.client.post(url, data=payload, **self.authorization_header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "test_playlist")
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["songs"], [])

