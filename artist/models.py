from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)


    def get_songs(self):
        return self.songs.all()

    def get_albums(self):
        return self.albums.all()

    def __str__(self):
        return self.name