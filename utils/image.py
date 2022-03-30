import os

def get_file_path(instance, filename):
    path = "music_cover/"
    filename = f"{instance.name}.jpeg"
    return os.path.join(path, filename)