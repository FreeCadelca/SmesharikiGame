import pygame

from config import config_parse
from .DefaultBar import DefaultBar


class IncrementBar(DefaultBar):
    BAR_HEIGHT = 75
    BAR_WIDTH = 500

    def __init__(self, name, pos, text, value=50, text_offset_x=0):
        super().__init__(name, pos, 'menu\\IncrementBar.png')
        self.text_offset_x = text_offset_x
        self.text = text
        self.value = value
        self.max_value = 100
        self.rect = self.image.get_rect(center=pos)

        pygame.font.init()
        my_font = pygame.font.Font('source\\' + config_parse()["font"], 30)
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
        self.image = self.primary_image.copy()  # resetting the image to a state without rendering a number
        pygame.font.init()
        my_font = pygame.font.Font('source\\' + config_parse()["font"], 30)

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
        self.value += delta
        if self.value > self.max_value:  # I can't write cyclic incrementing via % max_value
            self.value = 0  # so I should write this crutch(
        elif self.value < 0:
            self.value = self.max_value
