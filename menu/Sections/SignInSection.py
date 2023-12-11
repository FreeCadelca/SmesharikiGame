from ..Bars.DefaultBar import DefaultBar
from ..Bars.IncrementBar import IncrementBar
from .AbstractSection import AbstractSection
from ..Bars.LabelBar import LabelBar

from screen_data import *
from config import *


class SignInSection(AbstractSection):
    BARS_SIGNIN = ['Enter login...', 'Enter password...', 'Repeat password...', 'Confirm', 'Back']

    def __init__(self):
        super().__init__()
        cfg = config_parse()
        self.max_bars = len(SignInSection.BARS_SIGNIN)
        self.single_space = cfg['spacing']

        self.state_of_entering_text = 0
        # the state when the text is entered in the field.
        # 0 - nothing is being entered, 1 - login, 2 - 1st pass, 2 - 2nd pass

        for i in range(3):
            offset = (i - len(SignInSection.BARS_SIGNIN) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(SignInSection.BARS_SIGNIN) // 2)
            # spacing between bars
            new_bar = LabelBar(
                SignInSection.BARS_SIGNIN[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SignInSection.BARS_SIGNIN[i],
                text_color=(0, 153, 171),
                font_size=20
            )
            self.bars.append(new_bar)
        for i in range(3, len(SignInSection.BARS_SIGNIN)):
            offset = (i - len(SignInSection.BARS_SIGNIN) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(SignInSection.BARS_SIGNIN) // 2)
            # spacing between bars
            new_bar = LabelBar(
                SignInSection.BARS_SIGNIN[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SignInSection.BARS_SIGNIN[i])
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events):
        super().input(keys, last_pressed_keys, id_current_section, events)
        if self.state_of_entering_text:  # if we are typing text
            id_field = self.state_of_entering_text - 1
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        print(self.bars[id_field].text)
                        self.state_of_entering_text = 0
                    elif event.key == pygame.K_BACKSPACE:
                        self.bars[id_field].text = self.bars[id_field].text[:-1]
                    else:
                        self.bars[id_field].text += event.unicode
        else:
            if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
                if 0 <= self.current_bar < 3:
                    if self.bars[self.current_bar].text == SignInSection.BARS_SIGNIN[self.current_bar]:
                        self.bars[self.current_bar].text = ''
                        self.bars[self.current_bar].text_color = (0, 255, 100)
                        self.bars[self.current_bar].font_size = 28
                    self.state_of_entering_text = self.current_bar + 1
                    last_pressed_keys[pygame.K_RETURN] = True
                elif self.current_bar == 3:
                    pass
                    print('New user')
                    id_current_section = 1
                elif self.current_bar == 4:
                    id_current_section = 1
                    last_pressed_keys[pygame.K_UP] = True
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
        offset_of_current_bar = ((self.current_bar - len(SignInSection.BARS_SIGNIN) // 2) * DefaultBar.BAR_HEIGHT +
                                 self.single_space * (self.current_bar - len(SignInSection.BARS_SIGNIN) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'menu\\Stroke_700px.png'
        )
        bars_sprites.add(current_bar_sprite)
