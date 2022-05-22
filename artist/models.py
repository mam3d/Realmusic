from django.db import models
from user.models import User
from utils.image import get_file_path

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to=get_file_path, default="artist_iamge/default.png")
    genre = models.ForeignKey("music.Genre", on_delete=models.SET_NULL, null=True, blank=True)

    def get_songs(self):
        return self.songs.prefetch_related("artists", "views", "likes")

    def get_single_songs(self):
        return self.get_songs().filter(album=None)

    def get_albums(self):
        return self.albums.all()

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = [["user","artist"]]

    def __str__(self):
        return f"{self.user}-{self.artist} follow"
