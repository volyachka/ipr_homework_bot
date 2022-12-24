import pathlib


def file_exists(filename):
    return pathlib.Path(filename).exists()
