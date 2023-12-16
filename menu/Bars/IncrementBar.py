import pygame

from config import config_parse
from create_path_on_platform import *
from .DefaultBar import DefaultBar

"""
Class inherited from DefaultBar that describes a bar that displays text 
and a value that can be increased and decreased

Attributes:
    BAR_HEIGHT (int): The default height of the bar.
    BAR_WIDTH (int): The default width of the bar.
    name (str): The name of the bar. (in the code, not text on bar)
    pos (tuple): The position of the bar.
    image (pygame.Surface): The image of the bar.
    rect (pygame.Rect): The rectangle representing the position and size of the bar.
    text (str): The rendering text on the bar
    value (int): The value in bar
    max_value (int): The max value of bar
    primary_image (pygame.Surface): The original image

Methods:
    init: Initialize the IncrementBar object.
    update: Update the position and value of the bar.
    Updates the value of the IncrementBar. When the value exceeds max value, it resets to 0 and vice versa.
"""


class IncrementBar(DefaultBar):
    BAR_HEIGHT = 75
    BAR_WIDTH = 700

    def __init__(self, name, pos, text, value=50, text_offset_x=0):
        """
        Initialize the IncrementBar sprite

        Args:
            name (str): The name of the increment bar sprite
            pos (tuple): The initial position of the increment bar sprite (x, y)
            text (str): The text to be displayed on the increment bar
            value (int): The initial value of the increment bar (default is 50)
            text_offset_x (int): The offset for the text on the x-axis (default is 0)
        """
        super().__init__(name, pos, 'IncrementBar_700px.png')
        self.text_offset_x = text_offset_x
        self.text = text
        self.value = value
        self.max_value = 100
        self.rect = self.image.get_rect(center=pos)

        # Additional rendering for text and initial value on the bar
        pygame.font.init()
        my_font = pygame.font.Font(create_path_on_platform('fonts/' + config_parse()["font"]), 30)
        text_surface = my_font.render(
            self.text,
            False,
            (255, 240, 0)
        )
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        self.image.blit(
            text_surface,
            (IncrementBar.BAR_WIDTH // 2 - text_width // 2 + self.text_offset_x,
             IncrementBar.BAR_HEIGHT // 2 - text_height // 2))
        self.primary_image = self.image.copy()

    def update(self):
        """
        Update the position and image of the increment bar sprite
        """
        # Reset the image and render the updated value on the bar
        self.image = self.primary_image.copy()
        pygame.font.init()
        my_font = pygame.font.Font(create_path_on_platform('fonts/' + config_parse()["font"]), 30)

        value_surface = my_font.render(
            str(self.value),
            False,
            (255, 240, 0)
        )
        value_width = value_surface.get_width()
        value_height = value_surface.get_height()
        self.image.blit(
            value_surface,
            (IncrementBar.BAR_WIDTH - 80 - value_width, IncrementBar.BAR_HEIGHT // 2 - value_height // 2)
        )
        # method.blit changes the current image,
        # so I store the original image as primary_image and reset it to it before each rendering
        self.rect.center = self.pos

    def increment_value(self, delta):
        """
        Increment the value of the increment bar sprite by a given delta

        Args:
            delta (int): The value by which the increment bar's value will be incremented
        """
        self.value += delta
        if self.value > self.max_value:  # I can't write cyclic incrementing via % max_value
            self.value = 0  # so I should write this crutch(
        elif self.value < 0:
            self.value = self.max_value
