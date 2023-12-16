import pygame

from create_path_on_platform import *

"""
Class for the default bar sprite in the menu.

Attributes:
    BARHEIGHT (int): The default height of the bar.
    BARWIDTH (int): The default width of the bar.
    name (str): The name of the bar. (in the code, not text on bar)
    pos (tuple): The position of the bar.
    image (pygame.Surface): The image of the bar.
    rect (pygame.Rect): The rectangle representing the position and size of the bar.

Methods:
    init: Initializes the DefaultBar object.
    update: Updates the position of the bar.
"""


# Define the DefaultBar class
class DefaultBar(pygame.sprite.Sprite):
    BAR_HEIGHT = 75
    BAR_WIDTH = 700

    def __init__(self, name, pos, path):
        """
        Initialize the DefaultBar sprite

        Args:
            name (str): The name of the bar sprite
            pos (tuple): The initial position of the bar sprite (x, y)
            path (str): The path to the image file for the bar sprite
        """
        super().__init__()
        self.name = name
        self.pos = pos
        self.image = pygame.image.load(create_path_on_platform('menu/pictures/' + path))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """
        Updates the position of the bar.
        """
        self.rect.center = self.pos
