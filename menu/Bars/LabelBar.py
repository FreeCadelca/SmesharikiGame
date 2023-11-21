import pygame
from .DefaultBar import DefaultBar


class LabelBar(DefaultBar):
    BAR_HEIGHT = 75
    BAR_WIDTH = 500

    def __init__(self, name: str, pos, text: str, text_offset_x: int = 0):
        super().__init__(name, pos, 'menu\\DefaultBar.png')
        self.text = text
        self.text_offset_x = text_offset_x
        self.rect = self.image.get_rect(center=pos)
        self.primary_image = self.image.copy()

    def update(self):
        self.image = self.primary_image.copy()
        pygame.font.init()
        my_font = pygame.font.Font('source\\ARCADEPI.TTF', 30)
        text_surface = my_font.render(
            self.text,
            False,
            (255, 240, 0))
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        self.image.blit(
            text_surface,
            (LabelBar.BAR_WIDTH // 2 - text_width // 2 + self.text_offset_x,
             LabelBar.BAR_HEIGHT // 2 - text_height // 2)
        )
        self.rect.center = self.pos
