import pygame

from ..Bars.DefaultBar import DefaultBar
from ..Bars.LabelBar import LabelBar
from .AbstractSection import AbstractSection

from code_with_decoration.screen_settings import *
from config import *


"""
This class processes the "Main menu" section for the application

Attributes:
    BARS_MAIN_MENU (list): list containing names of bars in "Main menu" section.
    max_bars (int): maximum number of bars for the section.
    single_space (int): spacing for the bars.

Methods:
    input: method to handle user input
    setup_bars: method for drawing sprites
"""


class MainMenuSection(AbstractSection):
    BARS_MAIN_MENU = ['Play', 'Account', 'Settings', 'About us']

    def __init__(self):
        """
        The constructor for SignInSection class.
        """
        super().__init__()
        self.max_bars = 4
        cfg = config_parse()
        self.single_space = cfg['spacing']

        for i in range(len(MainMenuSection.BARS_MAIN_MENU)):
            offset = (i - len(MainMenuSection.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(MainMenuSection.BARS_MAIN_MENU) // 2)
            # spacing between bars
            new_bar = LabelBar(
                MainMenuSection.BARS_MAIN_MENU[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                MainMenuSection.BARS_MAIN_MENU[i])
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events, client):
        """
        Method to handle user input. Returns updated id_current_section, because we cannot rewrite int attribute
        of class Menu (self.id_current_section) bcs it mutable, so I return a new self.id_current_section value
        and assign it to the original each time, then check if something has changed

        Args:
            keys (dict): dictionary representing the pressed keys
            last_pressed_keys: dictionary representing the last pressed keys
            id_current_section (int): the current section id
            events: list of events in Pygame
            client (Client): the client object

        Returns:
            id_current_section (int): the updated current section id
        """
        super().input(keys, last_pressed_keys, id_current_section, events, client)
        if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
            if self.current_bar == 0:
                id_current_section = -1
            else:
                id_current_section = self.current_bar
            last_pressed_keys[pygame.K_RETURN] = True
        if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
            id_current_section = 0
            last_pressed_keys[pygame.K_ESCAPE] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False
        return id_current_section

    def setup_bars(self, bars_sprites, cfg: dict):
        """
        Method to set up all bars in the 'Main menu' section and append these sprites to bars_sprites,
        transmitted from Menu.

        Args:
            bars_sprites: the sprite group for bars from menu
            cfg (dict): dictionary of game configuration for the bars
        """
        super().setup_bars(bars_sprites, cfg)
        for i in self.bars:
            bars_sprites.add(i)
        offset_of_current_bar = ((self.current_bar - len(MainMenuSection.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT +
                                 self.single_space * (self.current_bar - len(MainMenuSection.BARS_MAIN_MENU) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'Stroke_700px.png'
        )
        bars_sprites.add(current_bar_sprite)
