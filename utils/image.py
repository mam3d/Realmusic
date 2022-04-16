import os

def get_file_path(instance, filename):
    from music.models import Song, PlayList

    if isinstance(instance, Song):
        path = "music_cover/"
    elif isinstance(instance, PlayList):
        path = "playlist/"
    else:
        path = "artist_image/"

    return os.path.join(path, filename)