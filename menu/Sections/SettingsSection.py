import pygame
from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar
from .AbstractSection import AbstractSection
from ..Bars.LabelBar import LabelBar


from screen_data import *
from key_scancodes import *
from configParse import *


class SettingsSection(AbstractSection):
    BARS_SETTINGS = ['Music volume', 'VFX volume', 'Left', 'Right', 'Jump']
    BARS_SETTINGS_TYPE = [IncrementBar, IncrementBar, LabelBar, LabelBar, LabelBar]

    def __init__(self):
        super().__init__()
        self.max_bars = 5
        self.state = 0  # 0 - default, 1,2,3 - choosing key for movement to the left, right, jump accordingly

        # for i in range(len(SettingsSection.BARS_SETTINGS)):
        #     offset = (i - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT
        #     # offset relative other bars
        #     spacing = 10 * (i - len(SettingsSection.BARS_SETTINGS) // 2)
        #     # spacing between bars
        #     new_bar = SettingsSection.BARS_SETTINGS_TYPE[i](
        #         SettingsSection.BARS_SETTINGS[i],
        #         (screen_width // 2, screen_height // 2 + (offset + spacing)),
        #         # 'menu\\Settings\\' + SettingsSection.BARS_SETTINGS[i] + '.png')
        #         'Menu\\DefaultBar.png')
        #     self.bars.append(new_bar)
        for i in range(2):
            offset = (i - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = 10 * (i - len(SettingsSection.BARS_SETTINGS) // 2)
            # spacing between bars
            new_bar = IncrementBar(
                SettingsSection.BARS_SETTINGS[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SettingsSection.BARS_SETTINGS[i] + ':',
                50,
                -IncrementBar.BAR_WIDTH * 0.08
            )
            self.bars.append(new_bar)
        for i in range(2, 5):
            offset = (i - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = 10 * (i - len(SettingsSection.BARS_SETTINGS) // 2)
            # spacing between bars
            new_bar = LabelBar(
                SettingsSection.BARS_SETTINGS[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SettingsSection.BARS_SETTINGS[i],
                -LabelBar.BAR_WIDTH * 0.25
            )
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events):
        if self.state == 0:  # if self.state == 0
            super().input(keys, last_pressed_keys, id_current_section, events)
            if keys[pygame.K_RIGHT] and not last_pressed_keys[pygame.K_RIGHT]:
                if SettingsSection.BARS_SETTINGS_TYPE[self.current_bar] == IncrementBar:
                    self.bars[self.current_bar].increment_value(5)
                last_pressed_keys[pygame.K_RIGHT] = True
            if keys[pygame.K_LEFT] and not last_pressed_keys[pygame.K_LEFT]:
                if SettingsSection.BARS_SETTINGS_TYPE[self.current_bar] == IncrementBar:
                    self.bars[self.current_bar].increment_value(-5)
                last_pressed_keys[pygame.K_LEFT] = True
            if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
                id_current_section = 0
                print('esc')
                last_pressed_keys[pygame.K_ESCAPE] = True
            if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
                if SettingsSection.BARS_SETTINGS_TYPE[self.current_bar] == LabelBar:
                    self.state = self.current_bar - 1
            for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
                # refreshing dict of last pressed keys
                if not keys[i]:
                    last_pressed_keys[i] = False
            return id_current_section
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.scancode in scancodes.keys():
                        print(
                            f'move {SettingsSection.BARS_SETTINGS[self.state + 1]} on key: {scancodes[event.scancode]}'
                        )
                        #  replacing key in config (to finish)
                        self.state = 0
            if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
                self.state = 0
                last_pressed_keys[pygame.K_ESCAPE] = True
            if keys[pygame.K_UP] and not last_pressed_keys[pygame.K_UP]:
                last_pressed_keys[pygame.K_UP] = True
            if keys[pygame.K_DOWN] and not last_pressed_keys[pygame.K_DOWN]:
                last_pressed_keys[pygame.K_DOWN] = True
            for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
                # refreshing dict of last pressed keys
                if not keys[i]:
                    last_pressed_keys[i] = False
            return id_current_section

    def setup_bars(self, bars_sprites):
        super().setup_bars(bars_sprites)
        for i in self.bars:
            bars_sprites.add(i)
        offset_of_current_bar = ((self.current_bar - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT +
                                 10 * (self.current_bar - len(SettingsSection.BARS_SETTINGS) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'menu\\Stroke.png'
        )
        bars_sprites.add(current_bar_sprite)
