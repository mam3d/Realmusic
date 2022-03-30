from django.db import models
from artist.models import Artist
from utils.image import get_file_path
class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=get_file_path, default="media/music_cover/default.png")
    artist = models.ManyToManyField(Artist, related_name="songs")
    url = models.URLField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name