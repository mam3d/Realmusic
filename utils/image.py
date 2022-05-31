import os

def get_file_path(instance, filename):
    path = f"{instance.__class__.__name__}/"
    return os.path.join(path, filename)