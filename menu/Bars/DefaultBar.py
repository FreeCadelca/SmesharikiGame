import pygame

from create_path_on_platform import *


class DefaultBar(pygame.sprite.Sprite):
    BAR_HEIGHT = 75
    BAR_WIDTH = 700

    def __init__(self, name, pos, path):
        super().__init__()
        self.name = name
        self.pos = pos
        self.image = pygame.image.load(create_path_on_platform('menu/pictures/' + path))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos
