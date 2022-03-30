
from django.db import models
from artist.models import Artist
from utils.image import get_file_path
from utils.validators import subtitle_validator
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


class Subtitle(models.Model):
    CHOICES = (
        ("P","Persian"),
        ("E","English"),
    )
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="subtitle")
    text = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, validators=[subtitle_validator])
    language = models.CharField(max_length=1, choices=CHOICES)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # File has to be saved inorder to read

        if self.file:
            with open(self.file.path, "r") as f:
                self.text = f.read()
            self.file.delete()
            self.save(*args, **kwargs)    

    def __str__(self):
        return f"{self.song.name}'s subtitle"