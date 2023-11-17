import pygame

from .Sections.MainMenuSection import MainMenuSection
from .Sections.AccountSection import AccountSection
from .Sections.SettingsSection import SettingsSection
from .Sections.AboutAssSection import AboutAssSection

from screen_data import *

class Menu:
    SECTIONS = [MainMenuSection, AccountSection, SettingsSection, AboutAssSection]

    def __init__(self, surface):
        self.bars_sprites = None
        self.surface = surface
        self.current_section = 0
        self.last_pressed_keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_RETURN: False,
            pygame.K_ESCAPE: False
        }
        self.section = MainMenuSection()

    def input(self):
        previous_section = self.current_section
        self.current_section = self.section.input(pygame.key.get_pressed(), self.last_pressed_keys,
                                                  self.current_section)
        if previous_section != self.current_section:
            print(previous_section, self.current_section)
            self.section = Menu.SECTIONS[self.current_section]()

    def setup_bars(self):
        self.bars_sprites = pygame.sprite.Group()
        self.section.setup_bars(self.bars_sprites)

    def run(self):
        self.setup_bars()
        self.input()
        self.bars_sprites.update()
        self.bars_sprites.draw(self.surface)
        # print(self.current_bar, self.current_section)
