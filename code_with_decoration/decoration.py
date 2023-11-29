from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTiles


class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('../graphics/tiles/sky_top.png').convert()
        self.middle = pygame.image.load('../graphics/tiles/sky_middle.png').convert()
        self.bottom = pygame.image.load('../graphics/tiles/sky_bottom.png').convert()
        self.horizon = horizon
        # растяжка картинки неба
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))


# class Lava:
#     def __init__(self, top, level_width):
#         lava_start = -screen_width
#         lava_tile_width = 192
#         tile_x_amount = int((level_width + screen_width) / lava_tile_width)
#         self.lava_sprites = pygame.sprite.Group()
#
#         for tile in range(tile_x_amount):
#             x = tile * lava_tile_width + lava_start
#             y = top
#             sprite = AnimatedTiles(192, x, y, '../graphics/tiles/lava')
#             self.lava_sprites.add(sprite)
#
#     def draw(self, surface, shift):
#         self.lava_sprites.update(shift)
#         self.lava_sprites.draw(surface)

