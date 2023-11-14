import pygame

from screen_data import *


class DefaultBar(pygame.sprite.Sprite):
    BAR_HEIGHT = 75
    BAR_WIDTH = 500

    def __init__(self, name, pos, path):
        super().__init__()
        self.name = name
        self.pos = pos
        self.image = pygame.image.load('source\\' + path)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos
        # print("hello")


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
            return 0
        elif keys[pygame.K_UP] and not last_pressed_keys[pygame.K_UP]:
            self.current_bar = (self.current_bar - 1) % self.max_bars
            last_pressed_keys[pygame.K_UP] = True
            return 0

    def setup_bars(self, bars_sprites):  # each section has setup_bars() func for drawing sprites
        pass


class MainMenuSection(AbstractSection):
    BARS_MAIN_MENU = ['Play', 'Account', 'Settings', 'About ass']

    def __init__(self):
        super().__init__()
        self.max_bars = 4

    def input(self, keys, last_pressed_keys, current_section):
        super().input(keys, last_pressed_keys, current_section)
        if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
            current_section = self.current_bar
            # print(current_section)
            last_pressed_keys[pygame.K_RETURN] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False
        return current_section
        # we cannot rewrite int attribute of class Menu (self.current_section) bcs it mutable,
        # so I return a new self.current_section value and assign it to the original each time,
        # then check if something has changed

    def setup_bars(self, bars_sprites):
        super().setup_bars(bars_sprites)
        for i in range(len(MainMenuSection.BARS_MAIN_MENU)):
            offset = ((i - len(MainMenuSection.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT +  # offset relative other bars
                      20 * (i - len(MainMenuSection.BARS_MAIN_MENU) // 2))  # spacing
            new_bar = DefaultBar(
                MainMenuSection.BARS_MAIN_MENU[i],
                (screen_width // 2, screen_height // 2 + offset),
                'menu\\' + MainMenuSection.BARS_MAIN_MENU[i] + '.png')
            bars_sprites.add(new_bar)

        offset_of_current_bar = ((self.current_bar - len(MainMenuSection.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT +
                                 20 * (self.current_bar - len(MainMenuSection.BARS_MAIN_MENU) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'menu\\Stroke.png'
        )
        bars_sprites.add(current_bar_sprite)

        # for i in self.bars_sprites:
        #     print(i.rect.center, end='; ')



class Menu:
    SECTIONS = [MainMenuSection]

    def __init__(self, surface):
        self.bars_sprites = None
        self.surface = surface
        self.current_section = 0
        self.last_pressed_keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_RETURN: False
        }
        self.section = MainMenuSection()

    def input(self):
        previous_section = self.current_section
        self.current_section = self.section.input(pygame.key.get_pressed(), self.last_pressed_keys, self.current_section)
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
