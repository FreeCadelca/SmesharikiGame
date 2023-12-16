import pygame
from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar

"""
This is an abstract class that provides a general description for specific section classes
to inherit from, enabling interaction with each class in the same way (polymorphism).

Attributes:
    max_bars (int): represents the maximum number of bars
    current_bar (int): the current bar
    bars (list): list of bars

Methods:
    input: method to handle user input
    setup_bars: method for drawing sprites
"""


class AbstractSection:
    def __init__(self):
        """
        The constructor for AbstractSection class.
        """
        self.max_bars = None
        self.current_bar = 0
        self.bars = []

    def input(self, keys, last_pressed_keys, id_current_section, events, client):
        """
        Method to handle user input.
        Each section has input() func for handling keys. two of actions can be written the same for all sections -
        it is a moving of current bar. After that remaining keys should be written separately for each section

        Args:
        keys: dictionary representing the pressed keys
        last_pressed_keys: dictionary representing the last pressed keys
        id_current_section (int): the current section id
        events: list of events in Pygame
        client (Client): the client object
        """
        if keys[pygame.K_DOWN] and not last_pressed_keys[pygame.K_DOWN]:
            self.current_bar = (self.current_bar + 1) % self.max_bars
            last_pressed_keys[pygame.K_DOWN] = True
        elif keys[pygame.K_UP] and not last_pressed_keys[pygame.K_UP]:
            self.current_bar = (self.current_bar - 1) % self.max_bars
            last_pressed_keys[pygame.K_UP] = True

    def setup_bars(self, bars_sprites, cfg: dict):  # each section has setup_bars() func for drawing sprites
        """
        Method to set up all bars in the 'About Us' section and append these sprites to bars_sprites,
        transmitted from Menu.

        Args:
            bars_sprites: the sprite group for bars from menu
            cfg (dict): dictionary of game configuration for the bars
        """
        pass
