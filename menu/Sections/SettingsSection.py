from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar
from .AbstractSection import AbstractSection
from ..Bars.LabelBar import LabelBar

from screen_data import *
from config import *


class SettingsSection(AbstractSection):
    BARS_SETTINGS = ['Music volume', 'VFX volume', 'Left', 'Right', 'Jump', 'Back']
    BARS_SETTINGS_TYPE = [IncrementBar, IncrementBar, LabelBar, LabelBar, LabelBar, LabelBar]

    def __init__(self):
        super().__init__()
        self.max_bars = 6
        self.state = 0  # 0 - default, 1,2,3 - choosing key for movement to the left, right, jump accordingly
        cfg = config_parse()
        self.single_space = cfg['spacing']
        for i in range(2):
            offset = (i - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(SettingsSection.BARS_SETTINGS) // 2)
            # spacing between bars
            new_bar = IncrementBar(
                SettingsSection.BARS_SETTINGS[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SettingsSection.BARS_SETTINGS[i] + ':',
                cfg[SettingsSection.BARS_SETTINGS[i]],
                -IncrementBar.BAR_WIDTH * 0.08
            )
            self.bars.append(new_bar)
        self.text_keys = [': ' + STR_TO_KEY_SIGN[cfg['controls'][i]] for i in cfg['controls']]
        for i in range(2, 5):
            offset = (i - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(SettingsSection.BARS_SETTINGS) // 2)
            # spacing between bars
            new_bar = LabelBar(
                SettingsSection.BARS_SETTINGS[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SettingsSection.BARS_SETTINGS[i] + self.text_keys[i - 2],
                0
            )
            self.bars.append(new_bar)
        for i in range(5, 6):
            offset = (i - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(SettingsSection.BARS_SETTINGS) // 2)
            # spacing between bars
            new_bar = LabelBar(
                SettingsSection.BARS_SETTINGS[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SettingsSection.BARS_SETTINGS[i],
                0
            )
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events):
        if self.state == 0:  # if self.state == 0
            super().input(keys, last_pressed_keys, id_current_section, events)
            if keys[pygame.K_RIGHT] and not last_pressed_keys[pygame.K_RIGHT]:
                if SettingsSection.BARS_SETTINGS_TYPE[self.current_bar] == IncrementBar:
                    self.bars[self.current_bar].increment_value(5)
                    config_edit([self.bars[self.current_bar].name], self.bars[self.current_bar].value)
                last_pressed_keys[pygame.K_RIGHT] = True
            if keys[pygame.K_LEFT] and not last_pressed_keys[pygame.K_LEFT]:
                if SettingsSection.BARS_SETTINGS_TYPE[self.current_bar] == IncrementBar:
                    self.bars[self.current_bar].increment_value(-5)
                    config_edit([self.bars[self.current_bar].name], self.bars[self.current_bar].value)
                last_pressed_keys[pygame.K_LEFT] = True
            if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
                id_current_section = 0
                last_pressed_keys[pygame.K_ESCAPE] = True
            if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
                if 1 < self.current_bar < 5:
                    self.state = self.current_bar - 1
                    self.bars[self.state + 1].text = 'Enter new key or esc...'
                else:
                    id_current_section = 0
            for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
                # refreshing dict of last pressed keys
                if not keys[i]:
                    last_pressed_keys[i] = False
            return id_current_section
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.scancode in SCANCODES.keys():
                        # if the key scancode is in the codes of our allowed keys, that is, in our list of scancodes
                        config_edit(
                            ['controls', SettingsSection.BARS_SETTINGS[self.state + 1]],
                            KEY_SIGN_TO_STR[SCANCODES[event.scancode]]
                            # see the instructions in pygame_dicts.py. It explains how the line above works
                        )
                        self.update_keys_text(config_parse())
                        self.state = 0
            if keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
                self.update_keys_text(config_parse())
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

    def setup_bars(self, bars_sprites, cfg):
        super().setup_bars(bars_sprites, cfg)

        for i in self.bars:
            bars_sprites.add(i)
        offset_of_current_bar = ((self.current_bar - len(SettingsSection.BARS_SETTINGS) // 2) * DefaultBar.BAR_HEIGHT +
                                 self.single_space * (self.current_bar - len(SettingsSection.BARS_SETTINGS) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'menu\\Stroke.png'
        )
        bars_sprites.add(current_bar_sprite)

    def update_keys_text(self, cfg):
        for i in range(2, 5):
            self.bars[i].text = (
                    SettingsSection.BARS_SETTINGS[i] +
                    ': ' +
                    STR_TO_KEY_SIGN[
                        cfg['controls'][SettingsSection.BARS_SETTINGS[i]]
                    ]
            )