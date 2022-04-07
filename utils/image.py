import os

def get_file_path(instance, filename):
    from music.models import Song
    path = "music_cover/" if isinstance(instance, Song) else "artist_image/"
    filename = f"{instance.name}.jpeg"
    return os.path.join(path, filename)