from csv import reader

import pygame

from create_path_on_platform import *
from code_with_decoration.screen_settings import tile_size
from os import walk


def import_folder(path):
    """
    This function imports images from the specified folder and returns a list of image surfaces.

    :param path: The path of the folder containing the images to be imported.
    :type path: str
    :return: List of image surfaces
    :rtype: list
    :raises: OSError if the path does not exist or other file-related errors

    The function iterates through the files in the specified folder and loads each image, converting it to
    a surface using the `pygame` library. The resulting image surfaces are then appended to the surface_list,
    which is returned after all images have been processed.
    """
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(create_path_on_platform(full_path)).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def import_csv_layout(path):
    """
    This function imports a CSV file containing a ground map layout and returns the map as a 2D list.

    :param path: The path of the CSV file to be imported.
    :type path: str
    :return: 2D list representing the ground map layout
    :rtype: list
    :raises: FileNotFoundError if the file does not exist, or other file-related errors

    The function first converts the 'path' to a platform-specific path using the 'create_path_on_platform' function.
    It then opens the file and uses the 'csv.reader' to read the CSV data, appending each row as a list to the
    'ground_map' list. The resulting 2D list representing the ground map layout is then returned.
    """
    path = create_path_on_platform(path)
    ground_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            ground_map.append(list(row))
        return ground_map


def import_cut_graphics(path):
    """
    This function imports a graphic file, cuts it into smaller tile-sized surfaces, and returns a list of these cut tiles.

    :param path: The path of the graphic file to be imported.
    :type path: str
    :return: List of tile-sized surfaces
    :rtype: list
    :raises: FileNotFoundError if the file does not exist, or other file-related errors

    The function first converts the 'path' to a platform-specific path using the 'create_path_on_platform' function.
    It then uses the 'pygame' library to load the image from the specified path and convert it to an alpha surface.
    The function then determines the number of tiles in the x and y directions based on the surface's size.
    It then iteratively creates new surfaces for each tile by using the 'pygame.Surface' and 'blit' methods,
    appending them to the 'cut_tiles' list. The resulting list contains the cut tile-sized surfaces,
    which is then returned.
    """
    path = create_path_on_platform(path)
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles
