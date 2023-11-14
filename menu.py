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
            last_pressed_keys[pygame.K_RETURN] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False

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
    BARS_MAIN_MENU = ['Play', 'Account', 'Settings', 'About ass']

    def __init__(self, surface):
        self.bars_sprites = None
        self.surface = surface
        self.current_bar = 0
        self.max_bar = 4
        self.current_section = 0
        self.last_pressed_keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_RETURN: False
        }

    def input_main_menu(self, keys):
        if keys[pygame.K_RETURN] and not self.last_pressed_keys[pygame.K_RETURN]:
            self.current_section = self.current_bar
            self.last_pressed_keys[pygame.K_RETURN] = True
            return 0

    def input_account(self, keys):
        if keys[pygame.K_ESCAPE]:
            self.current_section = 0
            self.current_bar = 0
            self.max_bar = 4

    def input_settings(self, keys):
        pass

    def input_about_ass(self, keys):
        pass

    def input(self):
        inputs = [self.input_main_menu,
                  self.input_account,
                  self.input_settings,
                  self.input_about_ass]
        keys = pygame.key.get_pressed()
        # Two of actions can be written the same for all sections - it is a moving of current bar.
        # After that remaining keys should be written separately for each section
        if keys[pygame.K_DOWN] and not self.last_pressed_keys[pygame.K_DOWN]:
            self.current_bar = (self.current_bar + 1) % self.max_bar
            self.last_pressed_keys[pygame.K_DOWN] = True
            return 0
        elif keys[pygame.K_UP] and not self.last_pressed_keys[pygame.K_UP]:
            self.current_bar = (self.current_bar - 1) % self.max_bar
            self.last_pressed_keys[pygame.K_UP] = True
            return 0
        inputs[self.current_section]()

        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN):
            # refreshing dict of last pressed keys
            if not keys[i]:
                self.last_pressed_keys[i] = False

    def setup_bars_main_menu(self):
        self.bars_sprites = pygame.sprite.Group()
        for i in range(len(Menu.BARS_MAIN_MENU)):
            offset = ((i - len(Menu.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT +  # offset relative other bars
                      20 * (i - len(Menu.BARS_MAIN_MENU) // 2))  # spacing
            new_bar = DefaultBar(
                Menu.BARS_MAIN_MENU[i],
                (screen_width // 2, screen_height // 2 + offset),
                'menu\\' + Menu.BARS_MAIN_MENU[i] + '.png')
            self.bars_sprites.add(new_bar)

        offset_of_current_bar = ((self.current_bar - len(Menu.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT +
                                 20 * (self.current_bar - len(Menu.BARS_MAIN_MENU) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'menu\\Stroke.png'
        )
        self.bars_sprites.add(current_bar_sprite)

        # for i in self.bars_sprites:
        #     print(i.rect.center, end='; ')

    def setup_bars_account(self):
        pass

    def setup_bars_settings(self):
        pass

    def setup_bars_about_ass(self):
        pass

    def setup_bars(self):
        setups = [self.setup_bars_main_menu,
                  self.setup_bars_account,
                  self.setup_bars_settings,
                  self.setup_bars_about_ass]
        setups[self.current_section]()

    def run(self):
        self.setup_bars()
        self.input()
        self.bars_sprites.update()
        self.bars_sprites.draw(self.surface)
        # print(self.current_bar, self.current_section)
