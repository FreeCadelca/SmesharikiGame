import pygame
from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar
from .AbstractSection import AbstractSection

from screen_data import *


class AccountSection(AbstractSection):
    BARS_ACCOUNT = ['Log in', 'Sign in', 'Log out']

    def __init__(self):
        super().__init__()
        self.max_bars = 3

    def input(self, keys, last_pressed_keys, current_section):
        super().input(keys, last_pressed_keys, current_section)
        if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
            current_section = 0
            print('esc')
            last_pressed_keys[pygame.K_UP] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False
        return current_section

    def setup_bars(self, bars_sprites):
        super().setup_bars(bars_sprites)
