from settings import *

def import_folder(*path):
    frames = []

    for folder_path, _, filenames in walk(join(*path)):
        for filename in sorted(filenames, key=lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, filename)
            frames.append(pg.image.load(full_path).convert_alpha())

    return frames

def import_image(*path, fmt = 'png', alpha = True):
    full_path = join(*path) + f'.{fmt}'

    return pg.image.load(full_path).convert_alpha() if alpha else pg.image.load(full_path)