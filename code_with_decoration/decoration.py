from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTiles, StaticTile
from support import import_folder
from random import choice, randint
from create_path_on_platform import *



class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load(create_path_on_platform('./graphics/tiles/Sky.png')).convert()
        # self.middle = pygame.image.load('./graphics/tiles/sky_middle.png').convert()
        # self.bottom = pygame.image.load('./graphics/tiles/sky_bottom.png').convert()
        self.horizon = horizon
        # растяжка картинки неба
        # self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size*11))
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size * 11))
        # self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size*11))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size * 11
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            # elif row == self.horizon:
            #     surface.blit(self.middle, (0, y))
            # else:
            #     surface.blit(self.bottom, (0, y))


class Lava:
    def __init__(self, top, level_width):
        lava_start = -screen_width
        lava_tile_width = 180
        tile_x_amount = int((level_width + screen_width * 2) / lava_tile_width)
        self.lava_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * lava_tile_width + lava_start
            y = top
            sprite = AnimatedTiles(192, x, y, create_path_on_platform('./graphics/tiles/lava'))
            self.lava_sprites.add(sprite)

    def draw(self, surface, shift):
        self.lava_sprites.update(shift)
        self.lava_sprites.draw(surface)


class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder(create_path_on_platform('./graphics/tiles/clouds'))
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
