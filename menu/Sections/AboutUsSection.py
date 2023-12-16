import pygame
from ..Bars.DefaultBar import DefaultBar
from .AbstractSection import AbstractSection

from code_with_decoration.screen_settings import *

"""
Сlass that represents the 'About us' section in the game menu.

Attributes:
    max_bars (int): the maximum number of bars

Methods:
    input: method to receive user input
    setup_bars: method to set up bars in the section
"""


class AboutUsSection(AbstractSection):
    def __init__(self):
        """
        The constructor for AboutUsSection class.
        """
        super().__init__()
        self.max_bars = 1

    def input(self, keys, last_pressed_keys: dict, id_current_section: int, events, client) -> int:
        """
        Method to receive user input.

        Args:
        keys: dictionary representing the pressed keys
        last_pressed_keys (dict): dictionary representing the last pressed keys
        id_current_section (int): the current section id (number)
        events: list of Pygame events in Game
        client (Client): the client object

        Returns:
        id_current_section (int): the updated current section id
        """
        super().input(keys, last_pressed_keys, id_current_section, events, client)
        if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
            id_current_section = 0
            last_pressed_keys[pygame.K_UP] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False
        return id_current_section

    def setup_bars(self, bars_sprites, cfg: dict):
        """
        Method to set up all bars in the 'About Us' section and append these sprites to bars_sprites,
        transmitted from Menu.

        Args:
        bars_sprites: the sprite group for bars
        cfg (dict): dictionary of game configuration for the bars
        """
        super().setup_bars(bars_sprites, cfg)
        newBar = DefaultBar(
            'image',
            (screen_width // 2, screen_height // 2),
            "AboutUs.png"
        )
        bars_sprites.add(newBar)
