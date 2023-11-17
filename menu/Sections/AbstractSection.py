import pygame
from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar


# An abstract class is a class that has a general description of some group of classes that will
# inherit from it. Thanks to this, we will be able to interact with each class from our class group
# in the same way (as with an abstract class). This is called polymorphism)))
class AbstractSection:
    def __init__(self):
        self.max_bars = None
        self.current_bar = 0

    def input(self, keys, last_pressed_keys, current_section):
        # each section has input() func for handling keys
        # Two of actions can be written the same for all sections - it is a moving of current bar.
        # After that remaining keys should be written separately for each section
        if keys[pygame.K_DOWN] and not last_pressed_keys[pygame.K_DOWN]:
            self.current_bar = (self.current_bar + 1) % self.max_bars
            last_pressed_keys[pygame.K_DOWN] = True
        elif keys[pygame.K_UP] and not last_pressed_keys[pygame.K_UP]:
            self.current_bar = (self.current_bar - 1) % self.max_bars
            last_pressed_keys[pygame.K_UP] = True

    def setup_bars(self, bars_sprites):  # each section has setup_bars() func for drawing sprites
        pass
