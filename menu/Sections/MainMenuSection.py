import pygame
from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar
from ..Bars.LabelBar import LabelBar
from .AbstractSection import AbstractSection

from screen_data import *


class MainMenuSection(AbstractSection):
    BARS_MAIN_MENU = ['Play', 'Account', 'Settings', 'About ass']

    def __init__(self):
        super().__init__()
        self.max_bars = 4

        for i in range(len(MainMenuSection.BARS_MAIN_MENU)):
            offset = (i - len(MainMenuSection.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = 10 * (i - len(MainMenuSection.BARS_MAIN_MENU) // 2)
            # spacing between bars
            new_bar = LabelBar(
                MainMenuSection.BARS_MAIN_MENU[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                MainMenuSection.BARS_MAIN_MENU[i])
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events):
        super().input(keys, last_pressed_keys, id_current_section, events)
        if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
            id_current_section = self.current_bar
            print("New section: ", id_current_section)
            last_pressed_keys[pygame.K_RETURN] = True
        if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
            id_current_section = 0
            print('esc')
            last_pressed_keys[pygame.K_ESCAPE] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False
        return id_current_section
        # we cannot rewrite int attribute of class Menu (self.id_current_section) bcs it mutable,
        # so I return a new self.id_current_section value and assign it to the original each time,
        # then check if something has changed

    def setup_bars(self, bars_sprites: pygame.sprite.Group):
        super().setup_bars(bars_sprites)
        for i in self.bars:
            bars_sprites.add(i)
        offset_of_current_bar = ((self.current_bar - len(MainMenuSection.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT +
                                 10 * (self.current_bar - len(MainMenuSection.BARS_MAIN_MENU) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'menu\\Stroke.png'
        )
        bars_sprites.add(current_bar_sprite)
        # for i in self.bars_sprites:
        #     print(i.rect.center, end='; ')
