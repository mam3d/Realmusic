
from django.db import models
from artist.models import Artist
from user.models import User
from utils.image import get_file_path
from utils.validators import subtitle_validator
from .managers import SongManager

class Genre(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=get_file_path, default="genre/default.png")

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=get_file_path, default="album/default.png")
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def get_songs(self):
        return self.songs.all()

    @property
    def total_songs(self):
        return self.songs.count()

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=get_file_path, default="music/default.png")
    artists = models.ManyToManyField(Artist, related_name="songs", blank=False)
    album = models.ForeignKey(Album,
                            related_name="songs",
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            )
    duration = models.FloatField()
    download_url = models.URLField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    objects = SongManager.as_manager()

    @property
    def total_views(self):
        return self.views.count()

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name





class Subtitle(models.Model):
    CHOICES = (
        ("P","Persian"),
        ("E","English"),
    )
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="subtitles")
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


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song =  models.ForeignKey(Song, on_delete=models.CASCADE, related_name="views", related_query_name="views")
    date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = [['user', 'song']]

    def __str__(self):
        return f"{self.user}-{self.song} view"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song =  models.ForeignKey(Song, on_delete=models.CASCADE, related_name="likes", related_query_name="likes")

    def __str__(self):
        return f"{self.user}-{self.song} like"
    class Meta:
        unique_together = [['user', 'song']]


class PlayList(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(default="playlist/default.png", upload_to=get_file_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)

    def __str__(self):
        return f"{self.user}-{self.name} playlist"