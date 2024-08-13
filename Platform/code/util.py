from settings import *

def import_folder(*path):
    frames = []

    for folder_path, _, files in walk(join(*path)):
        for filename in sorted(files, key=lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, filename)
            frames.append(pg.image.load(full_path).convert_alpha())

    return frames

def import_image(*path, fmt = 'png', alpha = True):
    full_path = join(*path) + f'.{fmt}'

    return pg.image.load(full_path).convert_alpha() if alpha else pg.image.load(full_path)

def import_audio(*path):
    audio_files = {}

    for folder_path, _, files in walk(join(*path)):
        for filename in files:
            audio_files[filename.split('.')[0]] = pg.mixer.Sound(join(folder_path, filename))

    return audio_files
