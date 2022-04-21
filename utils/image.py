import os

def get_file_path(instance, filename):
    from music.models import Song, PlayList, Album
    from artist.models import Artist

    if isinstance(instance, Song):
        path = "music_cover/"
    elif isinstance(instance, PlayList):
        path = "playlist/"
    elif isinstance(instance, Album):
        path = "album_cover/"
    elif isinstance(instance, Artist):
        path = "artist_image/"

    print(os.path.join(path, filename), flush=True)

    return os.path.join(path, filename)