from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar
from .AbstractSection import AbstractSection
from ..Bars.LabelBar import LabelBar

from screen_data import *
from config import *


class AccountSection(AbstractSection):
    BARS_ACCOUNT = ['Log in', 'Sign in', 'Log out', 'Back']

    def __init__(self):
        super().__init__()
        cfg = config_parse()
        self.variety_bars = ["Account: " + cfg["current_user"], "Coins: " + str(cfg["coins"])]
        if cfg["current_user"] == "guest":
            self.variety_bars += ['Log in', 'Sign in', 'Back']
        else:
            self.variety_bars += ['Log out', 'Back']
        self.max_bars = len(self.variety_bars)
        self.single_space = cfg['spacing']
        for i in range(2):
            offset = (i - len(self.variety_bars) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(self.variety_bars) // 2)
            # spacing between bars
            new_bar = LabelBar(
                self.variety_bars[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                self.variety_bars[i],
                text_color=(220, 220, 220),
                font_size=36
            )
            self.bars.append(new_bar)
        for i in range(2, len(self.variety_bars)):
            offset = (i - len(self.variety_bars) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(self.variety_bars) // 2)
            # spacing between bars
            new_bar = LabelBar(
                self.variety_bars[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                self.variety_bars[i])
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events, client):
        super().input(keys, last_pressed_keys, id_current_section, events, client)
        if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
            bar = self.variety_bars[self.current_bar]
            if bar == "Log in":
                id_current_section = 4
                last_pressed_keys[pygame.K_RETURN] = True
            elif bar == "Sign in":
                id_current_section = 5
                last_pressed_keys[pygame.K_RETURN] = True
            elif bar == "Log out":
                config_edit(["current_user"], "guest")
                config_edit(["coins"], 0)
                id_current_section = 0
                last_pressed_keys[pygame.K_RETURN] = True
            elif bar == "Back":
                id_current_section = 0
                last_pressed_keys[pygame.K_RETURN] = True
            last_pressed_keys[pygame.K_RETURN] = True
        elif keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
            id_current_section = 0
            last_pressed_keys[pygame.K_ESCAPE] = True
        for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
            # refreshing dict of last pressed keys
            if not keys[i]:
                last_pressed_keys[i] = False
        return id_current_section

    def setup_bars(self, bars_sprites, cfg):
        super().setup_bars(bars_sprites, cfg)
        for i in self.bars:
            bars_sprites.add(i)
        offset_of_current_bar = ((self.current_bar - len(self.variety_bars) // 2) * DefaultBar.BAR_HEIGHT +
                                 self.single_space * (self.current_bar - len(self.variety_bars) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'Stroke_700px.png'
        )
        bars_sprites.add(current_bar_sprite)
