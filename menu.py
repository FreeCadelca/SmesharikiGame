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
        # self.image = pygame.Surface((50, 50))
        # self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos
        # print("hello")

    def clickCheck(self, pos):
        if self.rect.left < pos[0] < self.rect.right and self.rect.top < pos[1] < self.rect.bottom:
            return True
        else:
            return False


class Menu:
    BARS_MAIN_MENU = ['Play', 'Skins', 'Settings', 'About ass']

    def __init__(self, surface):
        self.bars_sprites = None
        self.surface = surface
        self.current_bar = 0
        self.max_bar = 4
        self.current_section = 0
        self.last_key = None
        self.clickableBars = []

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.last_key != 'd':
            self.current_bar = (self.current_bar + 1) % self.max_bar
            self.last_key = 'd'
            return 0
        elif keys[pygame.K_UP] and self.last_key != 'u':
            self.current_bar = (self.current_bar - 1) % self.max_bar
            self.last_key = 'u'
            return 0
        elif keys[pygame.K_RETURN] and self.last_key != 'r':
            print(Menu.BARS_MAIN_MENU[self.current_bar])
            self.last_key = 'r'
            return 0
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_RETURN]:
            self.last_key = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for bar in self.clickableBars:
                    if bar.clickCheck(event.pos):
                        print(bar.name)
                        for i in range(len(Menu.BARS_MAIN_MENU)):
                            if Menu.BARS_MAIN_MENU[i] == bar.name:
                                self.current_bar = i
                                break


    def setup_bars_main_menu(self):
        self.bars_sprites = pygame.sprite.Group()
        self.clickableBars = []
        for i in range(len(Menu.BARS_MAIN_MENU)):
            offset = ((i - len(Menu.BARS_MAIN_MENU) // 2) * DefaultBar.BAR_HEIGHT +  # offset relative other bars
                      20 * (i - len(Menu.BARS_MAIN_MENU) // 2))  # spacing
            new_bar = DefaultBar(
                Menu.BARS_MAIN_MENU[i],
                (screen_width // 2, screen_height // 2 + offset),
                'menu\\' + Menu.BARS_MAIN_MENU[i] + '.png')
            self.bars_sprites.add(new_bar)
            self.clickableBars.append(new_bar)

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

    def setup_bars_skins(self):
        pass

    def setup_bars_settings(self):
        pass

    def setup_bars_about_ass(self):
        pass

    def setup_bars(self):
        setups = [self.setup_bars_main_menu,
                  self.setup_bars_skins,
                  self.setup_bars_settings,
                  self.setup_bars_about_ass]
        setups[self.current_section]()

    def run(self):
        self.setup_bars()
        self.input()
        self.bars_sprites.update()
        self.bars_sprites.draw(self.surface)
        # print(self.current_bar, self.current_section)
