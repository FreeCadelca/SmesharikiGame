import pygame
from ..Bars.DefaultBar import DefaultBar
from .AbstractSection import AbstractSection

from code_with_decoration.screen_settings import *


class AboutUsSection(AbstractSection):
    def __init__(self):
        super().__init__()
        self.max_bars = 1

    def input(self, keys, last_pressed_keys, id_current_section, events, client):
        super().input(keys, last_pressed_keys, id_current_section, events, client)
        if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
            id_current_section = 0
            last_pressed_keys[pygame.K_UP] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False
        return id_current_section

    def setup_bars(self, bars_sprites, cfg):
        super().setup_bars(bars_sprites, cfg)
        newBar = DefaultBar(
            'image',
            (screen_width // 2, screen_height // 2),
            "AboutUs.png"
        )
        bars_sprites.add(newBar)
