from csv import reader

import pygame

from create_path_on_platform import *
from settings import tile_size
from os import walk


def import_folder(path):
    """
    Imports a list of surfaces from an entire folder of images.

    Parameters:
    - path (str): The path to the folder containing images.

    Returns:
    - list: A list of pygame.Surface objects.
    """
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def import_csv_layout(path):
    """
    Imports a 2D list representing a level layout from a CSV file.

    Parameters:
    - path (str): The path to the CSV file.

    Returns:
    - list: A 2D list representing the level layout.
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
    Imports a list of cut tiles from a single image.

    Parameters:
    - path (str): The path to the image containing cut tiles.

    Returns:
    - list: A list of pygame.Surface objects representing cut tiles.
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
            new_surf = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles
