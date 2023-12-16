import pygame

from config import config_parse
from create_path_on_platform import *
from .DefaultBar import DefaultBar

"""
Class to create a labeled bar in a menu.

Attributes:
    BAR_HEIGHT (int): The default height of the labeled bar.
    BAR_WIDTH (int): The default of the labeled bar.

Methods:
    init: Initializes the LabelBar object with a name, position, text, text offset, text color, and font size.
    update: Updates the labeled bar with the specified text and characteristics.
"""

class LabelBar(DefaultBar):
    BAR_HEIGHT = 75
    BAR_WIDTH = 700

    def __init__(self, name: str, pos, text: str, text_offset_x: int = 0, text_color: tuple = (255, 240, 0),
                 font_size: int = 26):
        """
        Initializes the LabelBar object.

        Args:
            name (str): The name of the bar.
            pos (tuple): The position of the bar (x, y).
            text (str): The text to be displayed on the bar.
            text_offset_x (int): The offset for the text on the x-axis. The default value = 0
            text_color (tuple): The color of the text in RGB format. The default value = (255, 240, 0)
            font_size (int): The font size of the text. The default value = 26
        """
        super().__init__(name, pos, 'DefaultBar_700px.png')
        self.text = text
        self.text_offset_x = text_offset_x
        self.rect = self.image.get_rect(center=pos)
        self.primary_image = self.image.copy()
        self.text_color = text_color
        self.font_size = font_size

    def update(self):
        """
        Updates the labeled bar with the specified text and characteristics.
        """
        self.image = self.primary_image.copy()
        pygame.font.init()
        my_font = pygame.font.Font(create_path_on_platform('fonts/' + config_parse()["font"]), self.font_size)
        text_surface = my_font.render(
            self.text,
            False,
            self.text_color)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        self.image.blit(
            text_surface,
            (LabelBar.BAR_WIDTH // 2 - text_width // 2 + self.text_offset_x,
             LabelBar.BAR_HEIGHT // 2 - text_height // 2)
        )
        self.rect.center = self.pos
