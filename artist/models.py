from django.db import models
from django.template.defaultfilters import slugify
from utils.image import get_file_path

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(get_file_path, default="media/artist_iamge/default.png")
    genre = models.ForeignKey("music.Genre", on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(self, *args, **kwargs)

    def get_songs(self):
        return self.songs.all()

    def get_single_songs(self):
        return self.get_songs().filter(album=None)

    def get_albums(self):
        return self.albums.all()

    def __str__(self):
        return self.name