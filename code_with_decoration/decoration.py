from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTiles, StaticTile
from support import import_folder
from random import choice, randint
from create_path_on_platform import *



class Sky:
    """
    Represents the sky background in the game.

    Attributes:
    - top (pygame.Surface): The top part of the sky image.
    - horizon (int): The horizon level where the sky meets the ground.

    Methods:
    - __init__(self, horizon): Initializes a new Sky instance.
    - draw(self, surface): Draws the sky on the specified surface.
    """
    def __init__(self, horizon):
        """
        Initializes a new Sky instance.

        Parameters:
        - horizon (int): The horizon level where the sky meets the ground.
        """
        self.top = pygame.image.load(create_path_on_platform('./graphics/tiles/Sky.png')).convert()
        # self.middle = pygame.image.load('./graphics/tiles/sky_middle.png').convert()
        # self.bottom = pygame.image.load('./graphics/tiles/sky_bottom.png').convert()
        self.horizon = horizon
        # растяжка картинки неба
        # self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size*11))
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size * 11))
        # self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size*11))

    def draw(self, surface):
        """
        Draws the sky on the specified surface.

        Parameters:
        - surface (pygame.Surface): The surface where the sky will be drawn.
        """
        for row in range(vertical_tile_number):
            y = row * tile_size * 11
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            # elif row == self.horizon:
            #     surface.blit(self.middle, (0, y))
            # else:
            #     surface.blit(self.bottom, (0, y))


class Lava:
    """
    Represents a lava hazard in the game.

    Attributes:
    - lava_sprites (pygame.sprite.Group): Sprite group containing individual lava tiles.

    Methods:
    - __init__(self, top, level_width): Initializes a new Lava instance.
    - draw(self, surface, shift): Draws the lava on the specified surface with a horizontal shift.
    """
    def __init__(self, top, level_width):
        """
        Initializes a new Lava instance.

        Parameters:
        - top (int): The vertical position of the top of the lava.
        - level_width (int): The width of the game level.
        """
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
        """
        Draws the lava on the specified surface with a horizontal shift.

        Parameters:
        - surface (pygame.Surface): The surface where the lava will be drawn.
        - shift (int): The horizontal shift applied to the lava tiles.
        """
        self.lava_sprites.update(shift)
        self.lava_sprites.draw(surface)


class Clouds:
    """
    Represents a layer of clouds in the sky.

    Attributes:
    - cloud_sprites (pygame.sprite.Group): Sprite group containing individual cloud tiles.

    Methods:
    - __init__(self, horizon, level_width, cloud_number): Initializes a new Clouds instance.
    - draw(self, surface, shift): Draws the clouds on the specified surface with a horizontal shift.
    """
    def __init__(self, horizon, level_width, cloud_number):
        """
        Initializes a new Clouds instance.

        Parameters:
        - horizon (int): The vertical position where the clouds are placed.
        - level_width (int): The width of the game level.
        - cloud_number (int): The number of clouds to generate.
        """
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
        """
        Draws the clouds on the specified surface with a horizontal shift.

        Parameters:
        - surface (pygame.Surface): The surface where the clouds will be drawn.
        - shift (int): The horizontal shift applied to the cloud tiles.
        """
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
